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
    # historical_data()
    intent_data()
    test_data()

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

def general_conversation():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Conversation(sentence VARCHAR(300), response VARCHAR(300))"
    cur.execute("DROP TABLE IF EXISTS Conversation")
    cur.execute(query)
    with open('Conversation.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            sql_query = "INSERT INTO Conversation(sentence, response) VALUES(?,?);"
            sql_data = (row[0], row[1])
            cur.execute(sql_query, sql_data)
    conn.commit()
    conn.close()

def intent_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Intent_sentence(sentence VARCHAR(300), intent CHAR(1))"
    cur.execute("DROP TABLE IF EXISTS Intent_sentence")
    cur.execute(query)
    with open('Sentence_Intent.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            sql_query = "INSERT INTO Intent_sentence(sentence, intent) VALUES(?,?);"
            sql_data = (row[0], row[1])
            cur.execute(sql_query, sql_data)
    conn.commit()
    conn.close()

def historical_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Historical_data(origin CHAR(3), exp_dep VARCHAR(4), dep_delay INTEGER, destination CHAR(3), exp_arr VARCHAR(4), arr_delay INTEGER, month CHAR(2), day VARCHAR(8), toc CHAR(2))"
    cur.execute(query)
    conn.commit
    conn.close

def test_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Test_data(origin CHAR(3), exp_dep VARCHAR(4), dep_delay INTEGER, destination CHAR(3), exp_arr VARCHAR(4), arr_delay INTEGER, month CHAR(2), day VARCHAR(8), toc CHAR(2))"
    cur.execute(query)
    conn.commit
    conn.close

def training_model():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Model_data(model_name VARCHAR(50) PRIMARY KEY)"
    cur.execute("DROP TABLE IF EXISTS Model_data")
    cur.execute(query)
    conn.commit
    conn.close

##################################################################################################
#                                         Booking queries
##################################################################################################
def get_all_station():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Station?"
    cur.execute(sql_query,)
    rows = cur.fetchall()
    conn.close()
    return rows


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

##################################################################################################
#                                      Prediction queries
##################################################################################################
def add_historical_data(historical_data):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    sql_query = "INSERT INTO Historical_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    data = (historical_data[0], historical_data[1], historical_data[2], historical_data[3], historical_data[4],
     historical_data[5], historical_data[6], historical_data[7], historical_data[8])
    cur.execute(sql_query, data)
    conn.commit()
    conn.close()

def get_all_historical_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Historical_Data"
    cur.execute(sql_query)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_test_data(historical_data):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    sql_query = "INSERT INTO Test_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    data = (historical_data[0], historical_data[1], historical_data[2], historical_data[3], historical_data[4],
     historical_data[5], historical_data[6], historical_data[7], historical_data[8])
    cur.execute(sql_query, data)
    conn.commit()
    conn.close()

def get_all_test_data():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Test_data"
    cur.execute(sql_query)
    rows = cur.fetchall()
    conn.close()
    return rows

##################################################################################################
#                                      Reasoning queries
##################################################################################################
def get_all_intent_sentences():
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Intent_sentence"
    cur.execute(sql_query)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_intent_sentences(sentence):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()
    sql_query = "INSERT INTO Intent_sentence VALUES(?, ?)"
    data = (sentence[0], sentence[1])
    cur.execute(sql_query, data)
    conn.commit()
    conn.close()

def get_chat_response(chat):
    conn = connect_DB("chatbot.db")
    cur = conn.cursor()

    sql_query = "SELECT * FROM Conversation WHERE sentence = ?"
    sql_data = chat
    cur.execute(sql_query, sql_data)
    rows = cur.fetchall()
    conn.close()
    return rows
##################################################################################################
#                                           Testing
##################################################################################################
if __name__ == '__main__':
    setup_database()
    rows = get_station_name("Norwich")
    rows2 = get_station_code("NRW")

    # for row in rows:
    #     print(row[1])

    # for row in rows2:
    #     print(row[0])

    # test = ["NRW", "0500", 2, "LST", "0600", 4, "05", "6", "GE"]
    # add_historical_data(test)