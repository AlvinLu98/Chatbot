"""
Created on Sun Oct 27 13:25:49 2019

@author: Alvin Lu
"""
import spacy
import nltk

nlp = spacy.load("en_core_web_sm")

##################################################################################################
#                                   Basic sentence processing
##################################################################################################

#Takes the raw input and returns tokenized words  
def process_sentence(raw_input):
    doc = nlp(raw_input)
    tokens = nltk.word_tokenize(raw_input)
    tagged = nltk.pos_tag(tokens)
    
    print("############################### SpaCy ###############################")
    for token in doc:
        print(token.text, token.pos_, token.tag_, token.dep_)

    for ent in doc.ents:
        print(ent.text, ent.label_)

    print()
    print("############################### NLTK ###############################")
    for tags in tagged:
        print(tags)
    
    #return the tokenized and tagged words

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