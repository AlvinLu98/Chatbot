#Flask Lab session
#App to save modules
#written by G. Richards
#29:10:2016

from flask import Flask, render_template,request, jsonify
import NLP
import nltk
import submitForm as SF
import website_scraping as WS
import NeuralNetwork as NN
import calendar
import datetime

import numpy as np
import random

app = Flask(__name__)     
bookticket = ['book ticket', 'book train', 'get ticket', 'get train', 'booking train', 'grab ticket']
trainingCom = ['train you', 'training you', 'train chatbot', 'training chatbot']

@app.route('/')
def index():
    return render_template('index.html')
	
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/checkTraining', methods=['POST'])
def check_Training():
    train = ''
    if request.form['prompt'] == 'Yes':
        train = 'Yes'
    else:
        train = 'No'
    return jsonify(train = train)

@app.route('/send_message', methods=['POST'])
def send_message():
    sentence = request.form['message']
    botResponse = ''
    sent_tokens = nltk.sent_tokenize(sentence)
    book = ''
    delay = ''
    train = ''
    training_Prompt = ''

    for sentence in sent_tokens:
        triples, root = NLP.dependency(sentence)
        triples = list(triples)
        print(root)
        
        for triple in triples:
            print(triple[1],"(",triple[0][0], triple[0][1],", ",triple[2][0], triple[2][1],")")
        
        classification, verb, subject= NLP.processSent(triples, root)
        rows = NLP.getResponse(root, verb, subject, classification)
        print(verb, subject, classification)
        if len(rows) > 0:
            print(classification, ": ", verb, " ", subject)
            rand = random.randint(0, len(rows)-1)
            response = str(rows[rand])
            botResponse += response[2:-3] + "<br>"
        
        else:
            botResponse += "I have no idea how to respond to: "
            botResponse += sentence
            if classification == "Q":
                botResponse += "<br> Alternatively, you can go to <a href='https://www.thetrainline.com/en/help/'>Trainline's FAQ</a> to find out the answer"
            training_Prompt = 'Y'
            
        if classification == "A":
            book, delay, train = determine_Action(verb, subject)
            
    return jsonify(message = botResponse, book = book, delay = delay, train = train, training = training_Prompt, user=sentence)

def determine_Action(verb, subject):
    command = verb + " " + subject
    book = ''
    delay = ''
    train = ''
    
    if command in bookticket:
        book = 'Y'
    
    elif command in trainingCom:
        train = 'Y'
        
    elif command in "delayed train":
        delay = 'Y'
     
    return book, delay, train

@app.route('/get_Train_Details', methods=['POST'])
def get_Train_Details():
    org = request.form['orig']
    dest = request.form['dest']
    ticket_type = request.form['ticket_type']
    date = request.form['go_date']
    time = request.form['time']
    hour = request.form['hour']
    quart = request.form['quarter']
    quant = request.form['quantity']
    month = calendar.month_name[int(date[5:7])]
    month = month[0:3]
    date_convert = date[-2:] +"-" + month + "-" + date[2:4]
    url = ''
    if ticket_type == "single":
        url = SF.submitTrainLineForm_Single(org, dest, ticket_type, date_convert, time, hour, quart, quant)
        trains = WS.get_Sigle_TL(url)
        return jsonify(trains = trains, url=url, tick_type="single")
    elif ticket_type == "return":
        ret_date = request.form['ret_date']
        ret_time = request.form['ret_time']
        ret_hour = request.form['ret_hour']
        ret_quart = request.form['ret_quarter']
        month = calendar.month_name[int(ret_date[5:7])]
        month = month[0:3]
        ret_date_convert = ret_date[-2:] +"-" + month + "-" + ret_date[2:4]
        url = SF.submitTrainLineForm_Return(org, dest, ticket_type, date_convert, time, hour, quart, ret_date_convert, ret_time, ret_hour, ret_quart, quant)
        out_trains, in_trains = WS.get_Ret_TL(url)
        return jsonify(out_trains = out_trains, in_trains = in_trains, url=url, tick_type="return")
    elif ticket_type == "open":
        url = SF.submitTrainLineForm_Single(org, dest, ticket_type, date_convert, time, hour, quart, quant)
        trains = WS.get_OpenRet_TL(url)
        return jsonify(trains = trains, url=url, tick_type="open")
    
@app.route('/train_Bot', methods=['POST'])
def train_Bot():
    sentence = request.form['sentence']
    response = request.form['response']
    print(sentence, response)
    triples, root = NLP.dependency(sentence)
    triples = list(triples)
    classification, verb, subject= NLP.processSent(triples, root)
    NLP.trainBot_Resp(root, verb, subject, classification, response)
    return jsonify(message = "Thank you for making me smarter!")
    
@app.route('/train_delay', methods=['POST'])
def train_delay():
    orig = request.form['origin']
    dest = request.form['destination']
    date  = request.form['date']
    time = request.form['time']
    day = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[-2:]))
    day = day.today().weekday()
    prev, nxt, delay, estArr = WS.getLiveTrainInfo(orig, dest, date, time)
    if estArr == 0:
        message="Train is not operating!"
        print(message)
        return jsonify(message=message)
    else:
        message = "Current delay is: " + delay
        if(day < 5):
            day = "WEEKDAY"
        elif(day == 5):
            day = "SATURDAY"
        else:
            day = "SUNDAY"
        orig = orig.lower()
        dest = dest.lower()
        predicted = NN.predict(orig, dest, time, day, date[5:7], delay)
        message = "Predicted delay to your destination is: " + str(predicted)
        return jsonify(message=message)
    
    
if __name__ == '__main__':
    app.run(debug = True)