# mysql-geometry

mysqlのgeometry型を用いてポリゴンの内外判定を使ってみる。

# データ準備

[e-Stat](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200521&toukeiYear=2015&serveyId=A002005212015&datum=2000&coordsys=1&format=shape)のサイトから東京都の境界データをダウンロードして解凍し、`./data`ディレクトリにフォルダごと格納しておく。

# 環境構築

Python3, pipenv, dockerが必要です

```sh
pipenv sync
```

# mysqlサーバ立ち上げ

```sh
docker-compose up -d
```

# mysqlサーバを落とす

```sh
docker-compose down
```

# mysqlにログイン(必要あれば)

```sh
# localhostから
mysql -h 127.0.0.1 -uroot -prootpw
# 別のdockerコンテナから
mysql -h mysql_host -uroot -prootpw
# mysqlコンテナにログインしてアクセス
docker-compose exec mysql /bin/bash # mysqlコンテナにログイン
mysql -uroot -prootpw # mysqlにログイン
```

# Run

## insert data

```sh
# geometriesテーブルに東京都境界データ情報挿入
pipenv run python insert_data.py
```

## ポリゴンの内外判定

- クエリ

```mysql
-- データベース選択
use sample_db;
-- 35.67405, 139.77250が含まれる住所を検索
SELECT
    id,
    addressCode,
    address
FROM
    geometries
WHERE  ST_Contains(polygon, GeomFromText("POINT(139.77250 35.67405)")) = 1
;
```

- 結果

```
+-------+-------------+-----------------------------------+
| id    | addressCode | address                           |
+-------+-------------+-----------------------------------+
| 17256 | 13102003001 | 東京都中央区銀座１丁目            |
+-------+-------------+-----------------------------------+
1 row in set, 1 warning (0.09 sec)
```


