"""
Created on Sun Oct 27 13:25:49 2019

@author: Alvin Lu
"""
import nltk
import pandas
import spacy
import string
import re

from nltk import word_tokenize
from spacy.lang.en.stop_words import stopword

nlp = spacy.load("en_core_web_lg")

##################################################################################################
#                                   Basic sentence processing
##################################################################################################
def pre_processing(raw_input):
    raw_input = lower_case(raw_input)
    raw_input = remove_punct(raw_input)
    raw_input = replace_abbreviations(raw_input)
    return raw_input

#Takes the raw input and returns tokenized words  
def process_sentence(raw_input):
    print("############################### Tokenisation ###############################")
    raw_input = pre_processing(raw_input)
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

#Calculates the similarity between two words
def calculate_similarity(word_1, word_2):
    return 0

#Return the processed sentence depending on input
def process_intent(raw_input, intent):
    return 0

##################################################################################################
#                               Additional Sentence Proccessing
##################################################################################################

#Lower Case input scentence, For example: There is an APPLE!!! => there is an apple!!!
def lower_case(text):
    text_lowercase = text.lower()
    return text_lowercase

#Remove Punctuation of input scentence, For example: There is an APPLE!!! => there is an apple
def remove_punct(text):
    text_nopunct = "".join(
        [char for char in text if char not in string.punctuation])  # It will discard all punctuations
    return text_nopunct

#Deal with the abbreviations in scentence, For example: There's an apple = > there is an apple
def replace_abbreviations(text):
    # patterns that used to find or/and replace particular chars or words
    # to find chars that are not a letter, a blank or a quotation
    pat_letter = re.compile(r'[^a-zA-Z \']+')
    # to find the 's following the pronouns. re.I is refers to ignore case
    pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
    # to find the 's following the letters
    pat_s = re.compile("(?<=[a-zA-Z])\'s")
    # to find the ' following the words ending by s
    pat_s2 = re.compile("(?<=s)\'s?")
    # to find the abbreviation of not
    pat_not = re.compile("(?<=[a-zA-Z])n\'t")
    # to find the abbreviation of would
    pat_would = re.compile("(?<=[a-zA-Z])\'d")
    # to find the abbreviation of will
    pat_will = re.compile("(?<=[a-zA-Z])\'ll")
    # to find the abbreviation of am
    pat_am = re.compile("(?<=[I|i])\'m")
    # to find the abbreviation of are
    pat_are = re.compile("(?<=[a-zA-Z])\'re")
    # to find the abbreviation of have
    pat_ve = re.compile("(?<=[a-zA-Z])\'ve")

    new_text = pat_letter.sub(' ', text).strip().lower()  # 去符号，去字节前，和字节后的whitspaces（去无意义的空格），全部变小写
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text

#Use NLTK library to tokenize
def tokenize(text):
    tokens = word_tokenize(text)  # W+ means that either a word character (A-Za-z0-9_) or a dash (-) can go there.
    return tokens

#Use NLTK libray to indentify the POS Tagging of each word, For example-> going (tag: verb)
def pos_tag(tokenized_list):
    tag = nltk.pos_tag(tokenized_list)
    return tag

#Base on the tag, return the word by lemmatizer, For example: going (tag: verb) => go
def get_wordnet_pos(
        treebank_tag):  # https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return False

# Combine above function to lemmatize each [word: tag] pair from sentence
def lemmatizing(tokenized_tag_list):
    WordNetLemmatizer = nltk.WordNetLemmatizer()
    lemmatized = []
    for tokenized_tag in tokenized_tag_list:
        correct_pos = get_wordnet_pos(tokenized_tag[1])
        if correct_pos != False:
            lemmatized_word = WordNetLemmatizer.lemmatize(tokenized_tag[0], correct_pos)
            lemmatized.append(lemmatized_word)
        elif correct_pos == False:
            lemmatized.append(tokenized_tag[0])
    return lemmatized

#Remove meaning less stop words
def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopword]  # To remove all stopwords
    return text


#1. replace_abbreviations
#2. tokenize
#3. pos_tag
#4. lemmatizing (based on pos_tag)
#5. remove_stopwords

#6. Vectorizer (Unigram, Bigram, TF-IDF)

###############CountVectorizer###############
from sklearn.feature_extraction.text import CountVectorizer
def getCountVectorizer(data_X_Y):
    count_vect = CountVectorizer()
    X_counts = count_vect.fit_transform(data_X_Y['clean_sentence'])
    # print(X_counts.shape)          #这里可以调取矩阵的大小
    # print(count_vect.get_feature_names())      #这里可以调取每一个feature的名字
    X_counts_df = pandas.DataFrame(X_counts.toarray(), columns=count_vect.get_feature_names())
    #print(X_counts_df)
    # return X_counts_df
    return X_counts


###############Vectorizing Raw Data: N-Grams###############
def getNGramVectorizer(data_X_Y):
    ngram_vect = CountVectorizer(ngram_range=(2, 2))  # It applies only bigram vectorizer
    X_counts = ngram_vect.fit_transform(data_X_Y['clean_sentence'])
    X_counts_df = pandas.DataFrame(X_counts.toarray(), columns=ngram_vect.get_feature_names())
    #print(X_counts_df)
    # return X_counts_df
    return X_counts


###############Vectorizing Raw Data: TF-IDF###############
from sklearn.feature_extraction.text import TfidfVectorizer
def getTfidfVectorizer(data_X_Y):
    tfidf_vect = TfidfVectorizer()
    X_tfidf = tfidf_vect.fit_transform(data_X_Y['clean_sentence'])
    X_tfidf_df = pandas.DataFrame(X_tfidf.toarray(), columns=tfidf_vect.get_feature_names())
    #print(X_tfidf_df)
    # X_tfidf_feat = pandas.concat([data_X_Y['body_len'], data_X_Y['punct%'], pandas.DataFrame(X_tfidf.toarray())], axis=1)
    # return X_tfidf_df
    return X_tfidf

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