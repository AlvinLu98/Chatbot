"""
nlp.py

Natural Language Processing and Understanding component
"""
import nltk
from nltk.corpus import treebank
import re
import chatbot
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.linalg import norm

def tf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

# Tokenize input
def process_query(raw_input):
    return nltk.word_tokenize(strip_input(raw_input))

# Remove punctuation and formatting from user input
def strip_input(input):
    return re.sub(r'[^\w\s]','',input.lower())

# Time formatting, we want the time in a 24 hour format
def format_time(raw_time):
    t = None
    if "am" in raw_time:
        t = raw_time.replace("am", "")
    elif "pm" in raw_time:
        t = str(12 + int(raw_time.replace("pm", "")))
    elif ":" in raw_time:
        t = raw_time.split(":", 1)[0]
    else:
        t = raw_time

    return t

# Fixes any typos in the place names
def fix_station_names(places):
    f = open(r"data\UK-City.txt")
    get = f.read()
    citys = get.split('\n')
    clearSpell=[]

    if len(places)==2:
     if places[0] in citys:
       clearSpell.append(places[0])
     else:
       mostSimilarity = 0
       for city in citys:
            similarity = tf_similarity(city,places[0])
            if (similarity > mostSimilarity):
               mostSimilarity = similarity
               clearCity = city
       clearSpell.append(clearCity)
       print(mostSimilarity,clearCity)

     if places[1] in citys:
       clearSpell.append(places[1])
     else:
       mostSimilarity = 0
       for city in citys:
            similarity = tf_similarity(city,places[1])
            if (similarity > mostSimilarity):
               mostSimilarity = similarity
               clearCity = city
       clearSpell.append(clearCity)
       print(mostSimilarity,clearCity)

    return clearSpell
    

# Turn input into a list of useable information 
def process_parameters(raw_input, intent):
    if intent == "__label__bookingticket":
        return process_info_booking(raw_input) # Find the stations and date/time of booking from query
    elif intent == "__label__prediction":
        return process_info_prediction(raw_input) # Find delay info from query
    elif intent == "__label__reason":
        return process_info_staff(raw_input) # Find route blockage info from query
    
    return [] # Query doesn't require extra info

def process_info_booking(raw_input):
    tokens = nltk.word_tokenize(raw_input)
    tagged = nltk.pos_tag(tokens)

    data = []

    ners = nltk.ne_chunk(tagged,binary=False)

    places = []
    time = ""
    date = ""

    for ne in ners:

        if len(ne)>=2:
            if ne[1] == 'VB':
                data.append(ne[0])
            if ne[1] == 'CD':
                if "/" in ne[0]: # Date
                    date = ne[0]
                elif "." in ne[0]: # Date but wrong format
                    date = str.replace(ne[0], ".", "/")
                else: # Time
                    time = format_time(ne[0])

        if type(ne) is nltk.tree.Tree: # Location data
            if (ne.label() == 'GPE'):
                places.append(u' '.join([i[0] for i in ne.leaves()]))
                print(places)

    # Edge case handling, attempt to recover from poor user input
    # A start station is missing
    if len(places) == 0:
        chatbot.message("Please specify at least the destination of your ticket.")
        return [] # We need at least a destination so give up
    if len(places) == 1:
        places = ["Norwich"] + places

    # The date is missing
    if date == "":
        if ("tomorrow" in raw_input): # Handling for NLTK not picking up today/tomorrow as dates
            date = "Tomorrow"
        else:
            date = "Today"

    # The time is missing
    if time == "":
        # Handling for NLTK not picking up morning/afternoon/evening/noon
        if ("morning" in raw_input): 
            time = "9"
        elif ("afternoon" in raw_input): 
            time = "15"
        elif ("noon" in raw_input): 
            time = "12"
        # Use default
        else: 
            time = "18"

    fixedNames = fix_station_names(places)

    return [fixedNames[0], fixedNames[1], date, time]

def process_info_prediction(raw_input):
    tokens = nltk.word_tokenize(raw_input)
    tagged = nltk.pos_tag(tokens)

    data = []

    ners = nltk.ne_chunk(tagged,binary=False)

    places = []
    time = ""

    for ne in ners:

        if len(ne)>=2:
            if ne[1] == 'CD':
                if "/" in ne[0]: # Date
                    date = ne[0]
                elif "." in ne[0]: # Date but wrong format
                    date = str.replace(ne[0], ".", "/")
                else: # Time
                    time = format_time(ne[0])

        if type(ne) is nltk.tree.Tree: # Location data
            if (ne.label() == 'PERSON'):
                places.append(u' '.join([i[0] for i in ne.leaves()]))
            if (ne.label() == 'GPE'):
                places.append(u' '.join([i[0] for i in ne.leaves()]))
                print(places)


    f = open(r"data\UK-City.txt")
    get = f.read()
    citys = get.split('\n')

    if len(places)==3:
        if places[0] not in citys:
             mostSimilarity = 0
             for city in citys:
              similarity = tf_similarity(city,places[0])
              if (similarity > mostSimilarity):
                mostSimilarity = similarity
                clearCity = city
             places[0] = clearCity

        if places[1] not in citys:
             mostSimilarity = 0
             for city in citys:
              similarity = tf_similarity(city,places[1])
              if (similarity > mostSimilarity):
                mostSimilarity = similarity
                clearCity = city
             places[1] = clearCity

        if places[2] not in citys:
             mostSimilarity = 0
             for city in citys:
              similarity = tf_similarity(city,places[2])
              if (similarity > mostSimilarity):
                mostSimilarity = similarity
                clearCity = city
             places[2] = clearCity

    # Edge case handling, attempt to recover from poor user input
    # A start station is missing
    if len(places) < 2:
        chatbot.message("Please specify where you are travelling from, to and where you are currently at to receive a prediction.")
        return [] # We need at least a destination so give up
    if len(places) == 2:
        places = ["Norwich"] + places

    return places

def process_info_staff(raw_input):
    tokens = nltk.word_tokenize(raw_input)
    tagged = nltk.pos_tag(tokens)

    data = []

    ners = nltk.ne_chunk(tagged,binary=False)

    places = []
    blockage = ""
    request_type = ""

    for ne in ners:

        if len(ne)>=2:
            if ne[len(ne) - 1] == 'NNP':
                places.append(ne[0])

        if type(ne) is nltk.tree.Tree: # Location data
            if (ne.label() == 'PERSON'):
                places.append(u' '.join([i[0] for i in ne.leaves()]))
            if (ne.label() == 'GPE'):
                places.append(u' '.join([i[0] for i in ne.leaves()]))
            

    # Edge case handling, attempt to recover from poor user input
    # A start station is missing
    if len(places) < 2:
        chatbot.message("Please specify the two stations you wish to receive information about.")
        return []

    # Handling for NLTK not picking up partial/full
    if ("partial" in raw_input): 
        blockage = "partial"
    # Use default
    else: 
        blockage = "full"

    # Handling for NLTK not picking up advise/schedule
    if ("schedule" in raw_input): 
        request_type = "schedule"
    # Use default
    else: 
        request_type = "advise"

    chatbot.message(blockage)
    chatbot.message(places)
    chatbot.message(request_type)

    return [blockage, places[0], places[1], request_type]