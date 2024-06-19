import sqlite3
import pandas as pd
from accupass import scrap_accupass

accupass_df = scrap_accupass()

# Connect to DB and create a cursor
conn = sqlite3.connect('events.db')
cursor = conn.cursor()
# print('DB Init')

# create table
cursor.execute("DROP TABLE IF EXISTS ACCUPASS")

# Creating table
table = """ CREATE TABLE ACCUPASS (
			Name VARCHAR(255) NOT NULL,
			EventTime TEXT,
			Venue VARCHAR(255),
			Artists VARCHAR(255),
            ImageURL VARCHAR(255),
            PageURL VARCHAR(255),
            StartTime TEXT,
            EndTime TEXT
		); """

cursor.execute(table)
# print("Table is Ready")

# insert the data from the DataFrame into the SQLite table
accupass_df.to_sql('ACCUPASS', conn, if_exists='replace', index = False)

conn.commit()

# Printing pandas dataframe
# print(pd.read_sql('''SELECT * FROM ACCUPASS''', conn))


def find_concert(table_name, keyword):
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE Name LIKE '%{keyword}%'", conn)
    concert_name = df['Name'].to_string()
    return concert_name

def find_time(table_name, keyword):
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE Time LIKE '%{keyword}%'", conn)
    return df

# jazz = find_concert('ACCUPASS','爵士')
# print(jazz)


# Close the cursor
cursor.close()


# Close DB Connection irrespective of success
# or failure
conn.close()
# print('SQLite Connection closed')
