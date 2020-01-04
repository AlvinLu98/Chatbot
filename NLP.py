"""
Created on Sun Oct 27 13:25:49 2019

@author: Alvin Lu
"""
import nltk
import pandas
import spacy
import string
import re
import Database_controller as dc
import nltk
import datetime

from nltk.corpus import treebank
from spacy.lang.en.stop_words import stopword
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.neighbors import KNeighborsClassifier

from joblib import dump, load

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
    print("############################### Spacy tokenisation ###############################")
    raw_input = pre_processing(raw_input)
    doc = nlp(raw_input)
    for token in doc:
        print("%10s %10s %5s %5s %10s %10s %r" %(token.text, token.head.text, token.pos_, token.tag_, 
        token.dep_, token.lemma_, token.is_stop))
    print()

    print("############################### NLTK tokenisation ###############################")
    tokenized = nltk.word_tokenize(raw_input)
    tagged = nltk.pos_tag(tokenized)
    for tag in tagged:
        print(tag)

    get_entities_spacy(doc)
    get_dependencies_spacy(doc)
    get_dependencies_nltk(tagged)
    return doc, tagged

def get_entities_spacy(doc):
    print("############################### Spacy Entities ###############################")
    for ent in doc.ents:
        print(ent.text, ent.label_)
    print()
    return doc.ents

def get_dependencies_nltk(tagged):
    print("############################### NLTK Dependencies ###############################")
    chunks = nltk.ne_chunk(tagged)
    for chunk in chunks:
        print(chunk)
    print()
    return chunks

def get_dependencies_spacy(doc):
    print("############################### Spacy Dependencies ###############################")
    for chunk in doc.noun_chunks:
        print("%10s %10s %10s %10s" %(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text))
    print()
    return doc.noun_chunks

#Calculates the similarity between two words
def calculate_similarity(word_1, word_2):
    return 0

##################################################################################################
#                                        Error recovery
##################################################################################################
def train_station_model():
    rows = dc.get_all_station()
    names, codes = name_code_split(rows)
    names = preprocess_data(names)
    kNN = KNeighborsClassifier(n_neighbors=3, weights='distance')
    kNN.fit(names, codes)
    dump(kNN, "station_model.joblib")

def name_code_split(rows):
    names = []
    codes = []
    for code, name in rows:
        names.append(name)
        codes.append(code)
    return names, codes

def preprocess_data(text):
    vectoriser = HashingVectorizer(n_features=20)
    vector = vectoriser.transform(text)
    return vector

def predict(name):
    model = load("station_model.joblib")
    vectoriser = HashingVectorizer(n_features=20)
    vector = vectoriser.transform([name])
    return model.predict(vector)

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
    tokens = nltk.word_tokenize(text)  # W+ means that either a word character (A-Za-z0-9_) or a dash (-) can go there.
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
def process_train_booking(sentence):
    s, n = process_sentence(sentence)
    origin, destination = retrieve_org_dest(s, n)
    t_type = retrieve_ticket_type(sentence)
    date = retrive_date(sentence)
    hour, minute = retrive_time(sentence)
    date, hour= process_time_date(date, hour)
    return origin, destination, t_type, date, hour, minute

def retrieve_org_dest(s, n):
    entities = get_entities_spacy(s)
    dependencies = get_dependencies_spacy(s)
    origin = None
    destination = None
    for chunk in dependencies:
        if chunk.root.head.text == "to":
            destination = chunk.text
        elif chunk.root.head.text == "from":
            origin = chunk.text
    if origin == None or destination == None:
        locations = []
        for entity in entities:
            if entity.label_ == "GPE" or entity.label_ == "FAC":
                locations.append(entity.text)
        if len(locations) == 2:
            origin = location[0]
            destination = location[1]
    return origin, destination

def retrieve_ticket_type(sentence):
    if "single" in sentence:
        return "single"
    elif "return" in sentence:
        return "return"
    elif "open return" in sentence:
        return "open"
    else:
        return None

def retrive_date(sentence):
    #https://stackoverflow.com/questions/31088509/identifying-dates-in-strings-using-nltk
    date = re.findall(r'\d+\S\d+\S\d+', sentence)
    if not date:
        months = ['January','Febuary','March','April','May','June','July', 'August', 'September', 'October','November','December']
        date = re.findall(r"(?=(\b"+'\s\d+|'.join(months)+r"\s\d+\b))", sentence)
        for i, d in enumerate(date):
            day = re.findall(r"\d", d)[0]
            day = day.rjust(2, "0")
            month = re.findall(r"(\b"+'|'.join(months)+r"\b)", d)[0]
            month = month[:3]
            now  = datetime.datetime.now()
            year = str(now.year)[-2:]
            d = day+"-"+month+"-"+year
            date[i] = datetime.datetime.strptime(d, "%d-%b-%y")
            # date[i] = day+"-"+month+"-"+year 
        if not date:
            pattern = r"(\b\d+\S{2}\s\bof\b\s"+r'|\d+\S{2}\s\bof\b\s'.join(months)+r"\b)"
            date = re.findall(pattern, sentence)
            for i, d in enumerate(date):
                day = re.findall(r"\d", d)[0]
                day = day.rjust(2, "0")
                month = re.findall(r"(\b"+'|'.join(months)+r"\b)", d)[0]
                month = month[:3]
                now  = datetime.datetime.now()
                year = str(now.year)[-2:]
                d = day+"-"+month+"-"+year
                date[i] = datetime.datetime.strptime(d, "%d-%b-%y")
                # date[i] = day+"-"+month+"-"+year
    if not date:
        now  = datetime.datetime.now()
        if "today" in sentence:
            day = str(now.day)
            day = day.rjust(2, "0")
            month = str(now.month)
            month = month.rjust(2, "0")
            year = str(now.year)[-2:]
            date = day+"-"+month+"-"+year
            date = [datetime.datetime.strptime(date, "%d-%m-%y")]
        elif "tomorrow" in sentence:
            tomorrow = now + datetime.timedelta(days=1)
            day = str(tomorrow.day)
            day = day.rjust(2, "0")
            month = str(tomorrow.month)
            month = month.rjust(2, "0")
            year = str(tomorrow.year)[-2:]
            date = day+"-"+month+"-"+year
            date = [datetime.datetime.strptime(date, "%d-%m-%y")]
    return date

def retrive_time(sentence):
    time = re.findall(r'\d{2}:\d{2}', sentence)
    hour = [None for i in range(len(time))]
    minute = [None for i in range(len(time))]
    if time is not None:
        for i, t in enumerate(time): 
            hour[i] = int(t[:2])
            minute[i] = int(t[-2:])
    if not time:
        if "now" in sentence:
            now  = datetime.datetime.now()
            hour = [now.hour]
            minute = [now.minute]
    for i, m in enumerate(minute):
        if m != 0:
            if m < 15:
                minute[i] = 15
            elif m < 30:
                minute[i] = 30
            elif m < 45:
                minute[i] = 45
            else:
                minute[i] = 0
                hour[i] = hour[i] + 1
    return hour, minute

def process_time_date(date, hour):
    if len(date) == len(hour):
        for i, d in enumerate(date):
            if hour is not None and hour[i] > 23:
               date[i] = d + datetime.timedelta(days=1)
               hour[i] = 0
    return date, hour
            
    
        
##################################################################################################
#                                     Train delay processing
###################################################################################################
#Extract train delay info from the sentence
def process_train_delay(sentence):
    return 0

##################################################################################################
#                                   Staff function processing
##################################################################################################
#Extract staff info from the sentence
def processs_contingencies(sentence):
    return 0

##################################################################################################
#                                           Testing
##################################################################################################

def main():
    sentence = input("Please enter something: ")
    process_sentence(sentence)

    print(process_train_booking(sentence))

    # train_station_model()
    # mistake = "Norwich"
    # print("Prediting spelling mistake for ", mistake)
    # print(predict(mistake))
    
if __name__ == '__main__':
    main()