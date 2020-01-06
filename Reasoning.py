from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.neighbors import KNeighborsClassifier
from experta import *
import Database_controller

from joblib import dump, load

intents = ['B', 'C', 'D']

def get_data():
    rows = Database_controller.get_all_intent_sentences()
    return rows

def preprocess(text):
    vectoriser = HashingVectorizer(n_features=20)
    vector = vectoriser.transform(text)
    return vector

def sentence_intent_split(rows):
    sentences = []
    intents = []
    for sentence, intent in rows:
        sentences.append(sentence)
        intents.append(intent)
    return sentences, intents

def train_model():
    rows = get_data()
    sentences, intents = sentence_intent_split(rows)
    sentences = preprocess(sentences)

    kNN = KNeighborsClassifier(n_neighbors=5, weights='distance')
    kNN.fit(sentences, intents)
    dump(kNN, "intent_model.joblib")

def predict(sentence):
    model = load("intent_model.joblib")
    vectoriser = HashingVectorizer(n_features=20)
    vector = vectoriser.transform([sentence])
    result = model.predict(vector)
    #https://stackoverflow.com/questions/37089177/probability-prediction-method-of-kneighborsclassifier-returns-only-0-and-1
    confidence = model.predict_proba(vector)[0][intents.index(result[0])]
    return result[0], confidence

def main():
    train_model()
    sentence = "Help"
    print(sentence)
    print(predict(sentence))

if __name__ == '__main__':
    main()