# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:23:50 2018

@author: Alvin Lu
"""

import nltk
from nltk.parse.corenlp import CoreNLPDependencyParser
import NLP

import numpy as np
import random

if __name__ == "__main__":
    chat = list()
    botResponse = "Hello, I'm a train booking chat-bot!\n"
    chat.append("bot: " + botResponse)
    print(botResponse)
    botResponse = "What's your name?"
    chat.append("bot: " + botResponse)
    print(botResponse)
    user = ">>"
    name = input(user)
    if name != " ":
        chat.append(name + ": " + name)
    else:
        name = "user"

    botResponse = "Hello " + name + "! How can I help?"
    chat.append("bot: " + botResponse)
    print(botResponse)
    while True:
        UInput = input(user)
        chat.append(name + ": " + UInput)
        sent_tokens = nltk.sent_tokenize(UInput)
        print(sent_tokens, "\n")
        
        if UInput.lower() == "goodbye":
                botResponse = "Thank you for speaking to me!\n"
                chat.append("bot: " + botResponse)
                print(botResponse)
                break

        for sentence in sent_tokens:
            triples, root = NLP.dependency(sentence)
            triples = list(triples)
            print(root)
            
            for triple in triples:
                print(triple[1],"(",triple[0][0], triple[0][1],", ",triple[2][0], triple[2][1],")")
            
            classification, verb, subject= NLP.processSent(triples, root)
            rows = NLP.getResponse(root, verb, subject, classification)

            if verb is None:
                print("Thank you ", name)
                chat.append("bot: " + botResponse)
                break
            
            elif len(rows) > 0:
                print(classification, ": ", verb, " ", subject)
                rand = random.randint(0, len(rows)-1)
                botResponse = str(rows[rand])
                chat.append("bot: " + botResponse[2:-3])
                print(botResponse[2:-3]) 
                if classification == "A":
                    NLP.determine_Action(verb, subject)
            
            else:
                print(classification, ": ", verb, " ", subject)
                botResponse = "I have no idea how to respond to: "
                botResponse += sentence
                chat.append("bot: " + botResponse)
                print(botResponse)
                while True:
                    botResponse = "Do you want to teach me how to repsond? Y/N\n"
                    helpResp =  input(botResponse)
                    chat.append("bot: " + botResponse)
                    helpResp = helpResp.upper()
                    chat.append(name + ": " + helpResp)
                    if helpResp == "Y":
                        NLP.trainBot(root, verb, subject, classification)
                        break
                    elif helpResp == "N":
                        botResponse = "Aww. Thanks though"
                        chat.append("bot: " + botResponse)
                        print(botResponse)
                        break
                    else:
                        botResponse = "Invalid repsonse!"
                        chat.append("bot: " + botResponse)
                        print(botResponse)
        
    print("------------------- CHAT HISTORY -------------------")
    for i in chat:
        print(i)
    