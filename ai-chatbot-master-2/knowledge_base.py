"""
knowledge_base.py

Knowledge Base component
"""

from pyknow import *
import knowledge_acquisition
import prediction

import chatbot
import knowledge_base_contingencies

class Statement(Fact):
    pass

class Response(KnowledgeEngine):
    information = []
    
    @Rule(Statement("__label__greet"))
    def answer_greeting(self):
        chatbot.message("Hello, I hope you are well.")
        
    @Rule(Statement("__label__bookingticket"))
    def answer_booking(self):
        if len(self.information) < 4:
            return # The user query was a mess and we didn't manage to salvage enough information

        start = self.information[0]
        destination = self.information[1]
        date = self.information[2]
        hour = self.information[3]
        
        # By default, we search for tickets today
        chatbot.message(f"You have asked me to find tickets from {start} to {destination}, {date.lower()} at {hour}:00.")
        
        chatbot.message("Just a moment while I search online for available tickets...")
        knowledge_acquisition.request_booking(start, destination, date, hour)
        
    @Rule(Statement("__label__prediction"))
    def answer_delay(self):
        chatbot.message(self.information)

        start = self.information[0]
        destination = self.information[1]
        at = self.information[2]

        #pre = prediction.predict_arrival_delay("Norwich", "London Liverpool Street", "Manningtree", 4.0)
        pre = prediction.predict_arrival_delay(start, destination, at, 0)

        chatbot.message(f"Calculating a prediction for the delay between {start} and {destination} currently at {at} with a current delay of {pre}...")
        chatbot.message(f"I predict a delay of {pre} minutes.")
    
    @Rule(Statement("__label__reason"))
    def answer_staff(self):
        info_type = self.information[3]
        blockage_type = self.information[0]
        start = self.information[1]
        destination = self.information[2]

        chatbot.message(f"Below is the guideline staff information regarding {info_type} information for {blockage_type} blockages between {start} and {destination}.")
        knowledge_base_contingencies.respond(self.information)

    @Rule(Statement("help"))
    def answer_help(self):
        chatbot.message("To book a ticket, enter a request such as \"I want to book a ticket to London tomorrow\". You can also provide further information such as start station, date (dd/mm/yyyy) and time.")
        chatbot.message("To predict a delay, enter a statement in the format \"I am delayed by 4 from Norwich to London, current at Manningtree\".")
        chatbot.message("To get staff information, enter a statement in the format \"I am delayed by 4 from Norwich to London, current at Manningtree\".")
        
    @Rule(Statement("unknown"))
    def answer_unknown(self):
        chatbot.message("I'm sorry but I can't understand you.")

def respond(intent, information_tokens):
    engine = Response()
    engine.information = information_tokens
    engine.reset()
    engine.declare(Statement(intent, information_tokens))
    engine.run()
