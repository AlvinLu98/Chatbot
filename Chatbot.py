from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, session
from random import randrange
import NLP, Reasoning, Database_controller, Delay_Prediction, Web_Scraping

app = Flask(__name__)
app.secret_key="AI_Chatbot"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message')
def process_message():
    sentence = request.form['message']
    sentence = NLP.pre_processing(sentence)
    response = Database_controller.get_chat_response(sentence)
    if len(response) != 0:
        intent = Reasoning.predict(sentence)
        if 'intent' in session:
            if session['intent'] == 'B':
                print(session['intent'])
                process_booking(sentence)
            elif session['intent'] == 'C':
                print(session['intent'])
                process_contingencies(sentence)
            elif session['intent'] == 'D':
                print(session['intent'])
                process_delay(sentence)
        else:
            session['intent'] = intent
    else:
        if len(response) > 1:
            i = randrange(len(response))
            return jsonify(message = response[i])
        else:
            return jsonify(message = response[0])


def process_booking(sentence):
    return 0

def process_contingencies(sentence):
    return 0

def process_delay(sentence):
    return 0

if __name__ == '__main__':
    app.run(debug = True)