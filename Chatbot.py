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

@app.route('/booking')
def process_booking(sentence):
    return 0

@app.route('/train contingencies')
def process_contingencies(sentence):

# multiple blockage points that alter the schedule and advise given
# between Diss to Ipswich(Full) and Stowmarket to Ipswich(Partial)

    sentence = request.form['blockage', 'origin', 'destination', 'intent']
    response = Database_controller.get_contingency(sentence)
    if len(response) != 0:
        if 'blockage' and 'origin' and 'destination' and 'intent' in session:
            if session['blockage'] == 'full':
                if session['origin'] == 'Diss' and session['destination'] == 'Ipswich':
                    if session['blockage'] == 'A':
                        print(session['intent'] == 'scheduleA')
                        print(session['intent'] == 'adviseA')
                        return jsonify()
                    if session['blockage'] == 'B':
                        print(session['intent'] == 'scheduleB')
                        print(session['intent'] == 'adviseB')
                        return jsonify()
                    if session['blockage'] == 'C':
                        print(session['intent'] == 'scheduleC')
                        print(session['intent'] == 'adviseC')
                        return jsonify()
                else:
                    print(session['intent'])
                    return jsonify()

            if session['blockage'] == 'partial':
                if session['origin'] == 'Stowmarket' and session['destination'] == 'Ipswich':
                    if session['blockage'] == 'A':
                        print(session['intent'])
                        print(session['intent'] == 'scheduleA')
                        print(session['intent'] == 'adviseA')
                        return jsonify()
                    if session['blockage'] == 'B':
                        print(session['intent'] == 'scheduleB')
                        print(session['intent'] == 'adviseB')
                        return jsonify()
                else:
                    print(session['intent'])
                    return jsonify()

@app.route('/delay')
def process_delay(sentence):
    return 0

if __name__ == '__main__':
    app.run(debug = True)