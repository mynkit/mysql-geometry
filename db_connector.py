"""mysqlへ接続してクエリを叩く関数.

Examples:
    >>> import db_connector
    >>> connect_info = {'user': 'root', 'password': 'rootpw', 'host': '127.0.0.1', 'port': 3306, 'db': 'sample_db'}
    >>> geometries = db_connector.read_sql('select * from geometries;', connect_info)

"""


import pandas as pd
from pandas.core.frame import DataFrame
from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

CON = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'


def execute(
    sql: str,
    connect_info: dict,
    logger: Logger = None
):
    """クエリを実行.

    Args:
        sql (str): クエリ
        connect_info (dict): 接続情報
            {
                'user': user,
                'password': password,
                'host': host,
                'port': port,
                'db': db,
            }
        commit (bool): クエリをcommitするか(接続が切れたあとも処理を持続させるか)
        logger (Logger): ロガー。default

    """
    if type(logger) is Logger:
        logger.info(f'Run Query. query: {sql}')
    engine = get_engine(connect_info)
    connect = engine.connect()
    connect.execute(sql)
    connect.close()


def read_sql(
    sql: str,
    connect_info: dict,
    logger: Logger = None
) -> DataFrame:
    """DBからデータをデータフレームで取得する.

    Args:
        sql (str): クエリ
        connect_info (dict): 接続情報
            {
                'user': user,
                'password': password,
                'host': host,
                'port': port,
                'db': db,
            }
        logger (Logger): ロガー。default None。

    Returns:
        DataFrame

    """
    if type(logger) is Logger:
        logger.info(f'Get Query Result as DataFrame. query: {sql}')
    engine = get_engine(connect_info)
    df = pd.read_sql(sql, engine)
    return df


def get_engine(connect_info: dict) -> Engine:
    """DBからデータをデータフレームで取得する.

    Args:
        connect_info (dict): 接続情報
            {
                'user': user,
                'password': password,
                'host': host,
                'port': port,
                'db': db,
            }

    Returns:
        Engine

    """
    con = CON.format(
        user=connect_info['user'],
        password=connect_info['password'],
        host=connect_info['host'],
        port=connect_info['port'],
        db=connect_info['db'],
    )
    engine = create_engine(con)
    return engine
