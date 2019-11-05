# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 01:20:41 2019

@author: Alvin Lu
"""

import sqlite3

#Sets up the knowledgebase tables
def setup_database():
    conn = sqlite3.connect('sentences.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS chat_table(id INTEGER PRIMARY KEY, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS question_table(id INTEGER PRIMARY KEY, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    cur.execute("CREATE TABLE IF NOT EXISTS statement_table(id INTEGER PRIMARY KEY, root_word VARCHAR(40), subject VARCHAR(40), verb VARCHAR(40), sentence VARCHAR(200))")
    
    conn.commit()
    conn.close()

#Adds a new sentence and response to the knowledgebase
#@root root word of the sentence returned by NLP
#@verb verb of the sentence returned by NLP
#@subject subject of the sentence returned by NLP
#@sentence response to this type of setence
#@classification of the sentence returned by NLP
def add_To_Database(root, verb, subject, sentence, classification):
    conn = sqlite3.connect('sentences.db')
    cur = conn.cursor()
    if classification == 'C':
        cur.execute("INSERT OR REPLACE INTO chat_table(root_word,subject,verb,sentence) VALUES (?,?,?,?)",(root, subject, verb, sentence))
    elif classification == 'Q':
        cur.execute("INSERT OR REPLACE INTO question_table(root_word,subject,verb,sentence) VALUES (?,?,?,?)",(root, subject, verb, sentence))
    elif classification == "A":
        cur.execute("INSERT OR REPLACE INTO statement_table(root_word,subject,verb,sentence) VALUES (?,?,?,?)",(root, subject, verb, sentence))
    conn.commit()
    conn.close()

#Get existing responses from the knowledgebase
#@root root word of the sentence returned by NLP
#@verb verb of the sentence returned by NLP
#@subject subject of the sentence returned by NLP
#OUTPUT list of response that fits the given root word, verb and subject
def get_from_Database(root, verb, subject, classification):
    conn = sqlite3.connect('sentences.db')
    cur = conn.cursor()
    if classification == 'C':
        cur.execute("SELECT sentence FROM chat_table WHERE root_word=? AND subject=? AND verb=?",(root, subject, verb))
    elif classification == 'Q':
        cur.execute("SELECT sentence FROM question_table WHERE root_word=? AND subject=? AND verb=?",(root, subject, verb))
    elif classification == "A":
        cur.execute("SELECT sentence FROM statement_table WHERE root_word=? AND subject=? AND verb=?",(root, subject, verb))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

#Gets existsing responses from the knowledgebase
#@root root word of the sentence returned by NLP
#@verb verb of the sentence returned by NLP
#OUTPUT list of response that fits the given root word and verb
def get_By_Verb(root, verb, classification):
    conn = sqlite3.connect('sentences.db')
    cur = conn.cursor()
    if classification == 'C':
        cur.execute("SELECT sentence FROM chat_table WHERE root_word=? AND verb=?",(root, verb))
    elif classification == 'Q':
        cur.execute("SELECT sentence FROM question_table WHERE root_word=? AND verb=?",(root, verb))
    elif classification == "A":
        cur.execute("SELECT sentence FROM statement_table WHERE root_word=? AND verb=?",(root, verb))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

#Gets existsing responses from the knowledgebase
#@root root word of the sentence returned by NLP
#@subject subject of the sentence returned by NLP
#OUTPUT list of response that fits the given root word and subject
def get_By_Subject(root, subject, classification):
    conn = sqlite3.connect('sentences.db')
    cur = conn.cursor()
    if classification == 'C':
        cur.execute("SELECT sentence FROM chat_table WHERE root_word=? AND subject=?",(root, subject))
    elif classification == 'Q':
        cur.execute("SELECT sentence FROM question_table WHERE root_word=? AND subject=?",(root, subject))
    elif classification == "A":
        cur.execute("SELECT sentence FROM statement_table WHERE root_word=? AND verb=?",(root, subject))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

###############################################################################
#                                  Main method
###############################################################################
if __name__ == "__main__":
    setup_database()
    conn = sqlite3.connect('sentences.db')
    cur = conn.cursor()
    
    print("-----------------------------------------------------------------")
    cur.execute("SELECT * FROM question_table")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print("-----------------------------------------------------------------")
    
    cur.execute("SELECT * FROM chat_table")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print("-----------------------------------------------------------------")
    
    cur.execute("SELECT * FROM statement_table")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print("-----------------------------------------------------------------")