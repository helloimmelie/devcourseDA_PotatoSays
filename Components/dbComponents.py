from Components.config import config 
import pymysql
from sqlalchemy import create_engine

def connectToDB():

    host = config['host']
    user = config['user']
    password = config['password']
    port = config['port']
    database = config['database']

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port
        )

    conn.autocommit(False)
    cur = conn.cursor()
    cur.execute('use devProj_final;')
    
    print(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

    return cur, engine

