import csv
import sqlite3
from sqlite3 import Error

##################################################################################################
#                                          Base functions
###################################################################################################
def connect_DB(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except Error as e:
            print(e)

#https://www.sqlitetutorial.net/sqlite-python/creating-database/
def setup_database():
    station_data()

def station_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Station")
    cur.execute("CREATE TABLE IF NOT EXISTS Station(code CHAR(3) PRIMARY KEY, name VARCHAR(50))")
    with open('station_codes.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            sql_query = "INSERT INTO Station(code, name) VALUES(?,?);"
            sql_data = (row[1], row[0])
            cur.execute(sql_query, sql_data)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()