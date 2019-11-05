# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 02:58:17 2018

@author: Alvin Lu
"""

from nltk.parse.corenlp import CoreNLPDependencyParser

import re
import utilities
import calendar
import submitForm as SF
import website_scraping as WS
import NeuralNetwork as NN

qtag = ['WRB', 'WP$', 'WP', 'WDT']
subj = ['nsubj', 'nsubjpass']
bookticket = ['book ticket', 'book train', 'get ticket', 'get train', 'booking train', 'grab ticket']
greeting = ['Good morning', 'Hello', 'Hi', 'Good afternoon', 'Good afternoon']
train = ['train you', 'training you', 'train chatbot', 'training chatbot']

#Process the sentence and returns the dependencies
#@sentence: sentences from user input
#OUTPUT:    triples of grammar relationship and root word
def dependency(sentence):
    sentence = sentence.lower()
    #java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
    #To initialise CoreNLPDependencyParser
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parse = dep_parser.raw_parse(sentence)
    dep = next(parse)
    return dep.triples(), dep.root["word"]

def isQuestion(setence):
    if setence.count("?") > 0:
        return True
    return False

#Reasoning engine
#@triples: triples of grammatical relationship
#@root:    root word of the sentence
#OUTPUT:   classification, verb and subject of the sentence
def processSent(triples, root):
    verb = ''
    subject = ''
    classification = ''
    
    for t in triples:
        if t[1] == 'compound':
            verb = t[2][0]
            subject = t[0][0]
            classification = 'A'
            break
        
        elif t[1] == 'dobj':
            verb = t[0][0]
            subject = t[2][0]
            classification = 'A'
            break
            
        elif t[1] == 'nmod':
            verb = t[0][0]
            subject = t[2][0]
            classification = 'A'
            break
        
        elif t[1] in subj and t[2][0] == "book"  and t[0][0] == "train":
            verb = t[2][0]
            subject = t[0][0]
            classification = 'A'
            break
            
        elif t[1] in subj and t[0][0] == "delayed" and t[2][0] == "train":
            print("----------------------------------------")
            verb = t[0][0]
            subject = t[2][0]
            classification = 'A'
            break
            
        elif t[1] in subj and t[0][1] in qtag:
            verb = t[0][0]
            subject = t[2][0]
            classification = 'Q'
            break
        
        elif t[1] in subj and t[2][1] in qtag:
            verb = t[2][0]
            subject = t[0][0]
            classification = 'Q'
            break
        
        elif t[1] == 'advmod' and t[2][1] in qtag:
            verb = t[2][0]
            subject = t[0][0]
            classification = 'Q'
            break
        
        elif t[1] == "det":
            verb = t[2][0]
            subject = t[0][0]
            classification = 'C'
            break
        
        else:
            verb = t[0][0]
            subject = t[2][0]
            classification = 'C'
    
    if verb == '' and subject == '':
        classification = 'C'
        
    
    #if classification == "A":
     #   determine_Action(verb, subject)
        
    return classification, verb, subject

def trainBot(root, verb, subject, classification):
    response = input("What should my reponse be?\n")
    utilities.add_To_Database(root, verb, subject, response, classification)
    print("Thank you for making me smarter!")
    
def trainBot_Resp(root, verb, subject, classification ,response):
    utilities.add_To_Database(root, verb, subject, response, classification)
    
def getResponse(root, verb, subject, classification):
    rows = utilities.get_from_Database(root, verb, subject, classification)
    if len(rows) > 0:
        return rows
    else:
        if classification == "Q":
            return utilities.get_By_Subject(root, subject, classification)
        else:
            return utilities.get_By_Verb(root, verb, classification)
    return None
###############################################################################
#                       Function for chatbot simulation
###############################################################################
def determine_Action(verb, subject):
    command = verb + " " + subject
    if command in bookticket:
        bookTrain()
    
    if command in train:
        training()
        
    if command in "delayed train":
        delayed_Train()
    
def bookTrain():
    org = input("What's your location of origin?\n")
    dest = input("What's your destination?\n")
    r = re.compile("^[0-9]{4}/[0-1][0-9]/[0-3][0-9]")
    while(True):
        date = input("What is the date you need the train? (yyyy/mm/dd)\n")
        if r.match(date):
            break
        else:
            print("invalid date!\n")
    month = calendar.month_name[int(date[5:7])]
    month = month[0:3]
    date_convert = date[-2:] +"-" + month + "-" + date[2:4]
    
    hour = input("Hour\n")
    quart = input("Quarter\n")
    quant = input("Quantity\n")
    print("Please wait...")
    url = SF.submitTrainLineForm_Single(org, dest, "single", date_convert, "depart after", hour, quart, quant)
    trains = WS.get_Sigle_TL(url)
    for t in trains:
        print(t)
    
def delayed_Train():
    org = input("Where are you now?\n")
    dest = input("What's your destination?\n")
    r = re.compile("^[0-9]{4}/[0-1][0-9]/[0-3][0-9]")
    while(True):
        date = input("What is the date? (yyyy/mm/dd)\n")
        if r.match(date):
            break
        else:
            print("invalid date!\n")
    day = input("WEEKDAY/SATURDAY?SUNDAY?\n")
    time = input("What's is the time of day?\n")
    month = input("What month is this?\n")
    delay = input("How long was the delay from the station\n")
    
    predicted = NN.predict(org, dest, time, day, month, delay)
    message = "Predicted delay to your destination is: " + str(predicted)
    print(message)
 
def training():
    print("------------------- TRAINING CHATBOT -------------------")
    while True:
        sentence = input("What is the sentence?\n")
        triples, root = dependency(sentence)
        for triple in triples:
            print(triple[1],"(",triple[0][0], triple[0][1],", ",triple[2][0], triple[2][1],")")
        classification, verb, subject = processSent(triples, root)
        print(classification, ": ", verb, " ", subject)
        trainBot(root, verb, subject, classification)
        cont =  input("Do you want to continue teaching? Y/N\n")
        cont = cont.upper()
        if cont == "N":
            print("------------------- TRAINING COMPLETE -------------------")
            break