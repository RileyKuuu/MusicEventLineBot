import sqlite3
import pandas as pd

from flask import g
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from accupass import scrap_accupass
SQLITE_DB_PATH = './backend/scraped.db'
SQLITE_DB_SCHEMA = './backend/init.sql'

'''
# 取得DB連線
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db
'''

# 建立資料庫table及儲存爬蟲資訊
def create_table():
    # 讀取DB Schema
    with open(SQLITE_DB_SCHEMA) as f:
        create_db_sql = f.read()

    # DB 連線
    conn = sqlite3.connect(SQLITE_DB_PATH)

    # 根據DB Schema建立Table
    conn.executescript(create_db_sql)

    # 由accupass.py內的函式取得爬蟲dataframe
    df = scrap_accupass()

    # 將爬蟲資料寫入Table
    conn.execute("PRAGMA foreign_keys = ON")

    # 插入資料進入DB
    df.to_sql('ACCUPASS', conn, if_exists='append', index=False)
    # conn.close()

    # conn.execute(
    #     'INSERT INTO members (account, password) VALUES ("sam", "0000")'
    # )

# 讀取資料庫資料
def get_data(keyword):
     db = sqlite3.connect(SQLITE_DB_PATH)
     cursor = db.cursor()
     cursor.execute(f"SELECT * FROM 'ACCUPASS' WHERE EventName LIKE '%{keyword}%'")
     data = cursor.fetchall()
     return str(data)

'''
# 先把SQL query def在這裏
def find_concert(table_name, keyword):
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE Name LIKE '%{keyword}%'", conn)
    concert_name = df['Name'].to_string()
    return concert_name
'''