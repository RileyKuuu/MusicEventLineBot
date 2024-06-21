import sqlite3
import pandas as pd
from accupass import scrap_accupass
from flask import g

SQLITE_DB_PATH = 'scraped.db'
SQLITE_DB_SCHEMA = 'init.sql'

def create_table():
    # 讀取DB Schema
    with open(SQLITE_DB_SCHEMA) as f:
        create_db_sql = f.read()

    # DB 連線
    conn = sqlite3.connect(SQLITE_DB_PATH)

    # 根據DB Schema建立Table
    with conn:
        conn.executescript(create_db_sql)

    # 由accupass.py內的函式取得爬蟲dataframe
    df = scrap_accupass()

    # 將爬蟲資料寫入Table
    with conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # 插入資料進入DB
        df.to_sql('ACCUPASS', conn, if_exists='append', index=False)
        conn.close()

        # conn.execute(
        #     'INSERT INTO members (account, password) VALUES ("sam", "0000")'
        # )

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db

def get_data(keyword):
     db = get_db()
     cursor = db.cursor()
     cursor.execute(f"SELECT * FROM 'ACCUPASS' WHERE Name LIKE '%{keyword}%'")
     data = cursor.fetchall()
     return str(data)

'''
# 先把SQL query def在這裏
def find_concert(table_name, keyword):
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE Name LIKE '%{keyword}%'", conn)
    concert_name = df['Name'].to_string()
    return concert_name
'''