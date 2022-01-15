"""geometriesテーブルに東京都の境界データ情報を挿入する."""

import geopandas
import numpy as np
import db_connector

CONNECT_INFO = {
    'user': 'root',
    'password': 'rootpw',
    'host': '127.0.0.1',
    'port': 3306,
    'db': 'sample_db',
}
SHAPEFILE_PATH = 'data/A002005212015DDSWC13/h27ka13.shp'

if __name__ == '__main__':
    # 一旦geometriesテーブルを空にしておく
    print('delete geometries table data.')
    db_connector.execute('DELETE FROM geometries;', CONNECT_INFO)
    print('read shape file & shape.')
    gdf = geopandas.read_file(SHAPEFILE_PATH)
    gdf['addressCode'] = gdf.apply(
        lambda x: str(x['PREF']) + str(x['CITY']) + str(x['S_AREA']), axis=1)
    gdf['address'] = gdf.apply(
        lambda x: x['PREF_NAME'] + x['CITY_NAME'] + (x['S_NAME'] if x['S_NAME'] is not None else ''), axis=1)
    geo_text_list = [
        f"('{r['addressCode']}', '{r['address']}', GeomFromText('{r['geometry']}'))" for _, r in gdf.iterrows()]
    # geo_text_listをひとつの要素数が100個くらいになるように分割
    geo_text_list_split = [list(_) for _ in np.array_split(
        geo_text_list, len(geo_text_list)//100)]
    # geometriesテーブルにレコード挿入
    print('insert into geometries.')
    print(f'num of inserted records: {len(geo_text_list)}')
    for _geo_text_list in geo_text_list_split:
        geo_text = ','.join(_geo_text_list)
        db_connector.execute(
            f'''
            INSERT INTO
                geometries
            (addressCode, address, polygon)
            VALUES
            {geo_text}
            ;
            ''', CONNECT_INFO)
    print('complete.')
