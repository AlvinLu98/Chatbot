"""
Created on Sun Oct 27 13:25:49 2019

@author: Alvin Lu
"""
import spacy

nlp = spacy.load("en_core_web_lg")

##################################################################################################
#                                   Basic sentence processing
##################################################################################################

#Takes the raw input and returns tokenized words  
def process_sentence(raw_input):
    print("############################### Tokenisation ###############################")
    doc = nlp(raw_input)
    for token in doc:
        print("%10s %10s %5s %5s %10s %10s %r" %(token.text, token.head.text, token.pos_, token.tag_, 
        token.dep_, token.lemma_, token.is_stop))
    print()

    get_entities(doc)
    get_dependencies(doc)

def get_entities(doc):
    print("############################### Entities ###############################")
    for ent in doc.ents:
        print(ent.text, ent.label_)
    print()
    return doc.ents

def get_dependencies(doc):
    print("############################### Dependencies ###############################")
    for chunk in doc.noun_chunks:
        print("%10s %10s %10s %10s" %(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text))
    print()
    return doc.noun_chunks

#Remove punctuation and cases from users
def filter_input():
    return 0

#Changes the format of the date entered
def format_date():
    return 0

#Calculates the similarity between two words
def calculate_similarity(word_1, word_2):
    return 0

#Return the processed sentence depending on input
def process_intent(raw_input, intent):
    return 0

##################################################################################################
#                                     Train booking processing
##################################################################################################
#Extract train booking info from the sentence
def train_booking():
    return 0

##################################################################################################
#                                     Train delay processing
###################################################################################################
#Extract train delay info from the sentence
def train_delay():
    return 0

##################################################################################################
#                                   Staff function processing
##################################################################################################
#Extract staff info from the sentence
def staff_info():
    return 0

##################################################################################################
#                                           Testing
##################################################################################################

def main():
    sentence = input("Please enter something: ")
    process_sentence(sentence)
    
if __name__ == '__main__':
    main()