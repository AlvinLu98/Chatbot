import csv
import sqlite3
from sqlite3 import Error

##################################################################################################
#                                         Setup functions
##################################################################################################
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
    general_conversation()
    historical_data()

def station_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    #https://www.quackit.com/sqlite/tutorial/drop_a_table.cfm
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

def booking_sentences():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS sentences(sentence VARCHAR(300) PRIMARY KEY, classification CHAR(1))"

def general_conversation():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Conversation(sentence VARCHAR(300), response VARCHAR(300))"
    cur.execute("DROP TABLE IF EXISTS Conversation")
    cur.execute(query)
    conn.commit
    conn.close

def historical_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Historical_data(origin CHAR(3), dep_delay INTEGER, destination CHAR(3), arr_delay INTEGER, month CHAR(2), day VARCHAR(8))"
    cur.execute("DROP TABLE IF EXISTS Historical_data")
    cur.execute(query)
    conn.commit
    conn.close

##################################################################################################
#                                         Booking queries
##################################################################################################
def get_station_name(station):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Station WHERE name = ?"
    cur.execute(sql_query, (station, ))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_station_code(code):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Station WHERE code = ?"
    cur.execute(sql_query, (code, ))
    rows = cur.fetchall()
    conn.close()
    return rows

def add_historical_data(historical_data):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "INSERT INTO Historical_data VALUES ? ? ? ? ? ?"
    cur.execute(sql_query, (historical_data[0], historical_data[1], historical_data[2],
    historical_data[3], historical_data[4], historical_data[5]))
    conn.commit
    conn.close

##################################################################################################
#                                           Testing
##################################################################################################
if __name__ == '__main__':
    setup_database()
    rows = get_station_name("Norwich")
    rows2 = get_station_code("NRW")

    for row in rows:
        print(row[1])

    for row in rows2:
        print(row[0])