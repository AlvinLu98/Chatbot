import nltk
from nltk.corpus import treebank
import sys
import sklearn

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.linalg import norm
import fasttext

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



sentence = """i want to go to London."""


classifier = fasttext.load_model('intent_model.bin', label_prefix='__label__')

result = classifier.predict_proba([sentence],k=1)



print(result[0][0][0])

if result[0][0][0] == 'train_ticket_booking':



    token = nltk.sent_tokenize(sentence)
    tokens = nltk.word_tokenize(sentence)
    print(token)
    print(tokens)

    tagged = nltk.pos_tag(tokens)
    print(tagged[0:])

    #ners = nltk.ne_chunk(tagged,binary=True)
    #ners.draw()


    '''
    data = []
    places = []
    time = []
    
    for tag,pos in tagged:
        if pos == 'VB':
            data.append(tag)
    
    for tag,pos in tagged:
        if pos == 'NNP':
            places.append(tag)
    
    for tag,pos in tagged:
        if pos == 'CD':
            time.append(tag)
    
    data = [data] + [places] + [time]
    print(data)
    '''


    ners = nltk.ne_chunk(tagged,binary=False)
    #nerss.draw()

    intend = [result[0][0][0]]
    places = []
    time = []

    print(ners)

    for ne in ners:

        if type(ne) is nltk.tree.Tree:
           if (ne.label() == 'GPE'):
                places.append(u' '.join([i[0] for i in ne.leaves()]))
        if len(ne)>=2:
            if ne[1] == 'CD':
              time.append(ne[0])


    f = open("data/UK-City.txt")
    get = f.read()
    citys = get.split('\n')

    clearSpell=[]
    if len(places)==1:
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
      if places[0] in citys:
       clearSpell = []

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

     if places[0] in citys:
       if places[1] in citys:
         clearSpell = []



    data = [intend] + [places] + [time] + [clearSpell]

    print(data)

else:

    data = [result[0][0][0]]
    print(data)


'''
chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
chunkParser = nltk.RegexpParser(chunkGram)
chunked = chunkParser.parse(tagged)


for subtree in chunked.subtrees(filter=lambda t:t.label()=='Chunk'):
    print(subtree)

'''



