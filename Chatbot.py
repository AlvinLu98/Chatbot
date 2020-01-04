from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, session
from random import randrange
import NLP, Reasoning, Database_controller, Delay_Prediction, Web_Scraping

app = Flask(__name__)
app.secret_key="AI_Chatbot"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    sentence = request.form['chat']
    sentence = NLP.pre_processing(sentence)
    response = Database_controller.get_chat_response(sentence)
    if len(response) == 0:
        if 'state' in session:
            response = handle_intent(sentence)
        else:
            intent = Reasoning.predict(sentence)
            session['state'] = intent
            handle_intent(sentence)
    else:
        if len(response) > 1:
            i = randrange(len(response))
            return jsonify(message = response[i])
        else:
            return jsonify(message = response[0])

def handle_intent(sentence):
    if session['state'] == 'B':
        response = process_booking(sentence)
    elif session['state'] == 'C':
        response = process_contingencies(sentence)
    elif session['state'] == 'D':
        response = process_delay(sentence)
    else:
        response = "I'm not sure what to do"
    return response

def process_booking(sentence):
    origin, destination, t_type, date, hour, minute, amount = NLP.process_train_booking(sentence)

def process_contingencies(sentence):
    origin, destination, blockage, intent = NLP.processs_contingencies(sentence)

def process_delay(sentence):
    origin, destination, dep_time, dep_delay, arr_time, month, day = NLP.process_train_delay(sentence)

def quit_process():
    return 0

if __name__ == '__main__':
    app.run(debug = True)