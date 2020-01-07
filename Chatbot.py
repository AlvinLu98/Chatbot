#Functions from Flask
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, Response

#Importing other python files
import NLP, Reasoning, Database_controller, Delay_Prediction, Web_Scraping, Disruption_Contingencies, Form_Automation, Weather

#Other functions
from datetime import datetime
from random import randrange

#Initiating flask
app = Flask(__name__)
app.secret_key="AI_Chatbot"

#List of intents the chatbot recognises
intents = {
    'B' : 'Booking a ticket',
    'C' : 'Getting contingencies',
    'D' : 'Delay prediction',
    'W' : 'Checking weather'
}

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    sentence = request.form['message']
    if "Quit" in sentence:
        session.clear()
        return jsonify(message = "Current running task ended, Goodbye!")
    response = Database_controller.get_chat_response(sentence)
    if len(response) == 0:
        if 'state' in session:
            print(session)
            response = handle_intent(sentence)
            return jsonify(message = response)
        else:
            intent, prob = Reasoning.predict(sentence)
            if(prob > 0.9):
                Database_controller.add_intent_sentences(sentence, intent)
                Reasoning.train_model()
                session['state'] = intent
                response = intents[intent] + "<br/>"
                response = response + handle_intent(sentence)
                return jsonify(message = response)
            else:
                session['state'] = "T"
                session['train_sent'] = sentence
                response = "I'm not sure what you are trying to do. Please enter either 'Booking', 'Contingencies, 'Delay', 'Casual' or 'Weather' to let me know what was your intent"
                return jsonify(message = response)
    else:
        if len(response) > 1:
            i = randrange(len(response))
            return jsonify(message = response[i][1])
        else:
            return jsonify(message = response[0][1])

##################################################################################################
#                                        Intent processing
##################################################################################################
def handle_intent(sentence):
    if session['state'] == 'B':
        response = process_booking(sentence)
    elif session['state'] == 'C':
        response = process_contingencies(sentence)
    elif session['state'] == 'D':
        response = process_delay(sentence)
    elif session['state'] == 'T':
        response = process_training(sentence)
    elif session['state'] == 'T_C':
        response = train_conversation(sentence)
    elif session['state'] == 'W':
        response = process_weather(sentence)
    else:
        response = "I'm not sure what to do"
    return response

def process_booking(sentence):
    data_list = ['Origin', 'Destination', 'Ticket Type', 'Date', 'Hour', 'Minute', 'Amount of tickets']
    data_list_return = ['Origin', 'Destination', 'Ticket Type', 'Departure Date', 'Departure Hour',
     'Departure Minute', 'Amount of tickets', 'Return Date', 'Return Hour', 'Return Minute']
    
    origin, destination, t_type, date, hour, minute, amount = NLP.process_train_booking(sentence)


    check = handle_ticket_types(origin, destination, t_type, date, hour, minute, amount, data_list, data_list_return)
    if check is None:
        if session['Ticket Type'] == "return":
            values = get_data(data_list_return)
            form_filler = Form_Automation.Form_filler()
            url = form_filler.return_ticket('https://www.thetrainline.com/', values[0], values[1], values[2], values[3].strftime("%d/%m/%y"), values[4], values[5], values[7].strftime("%d/%m/%y"), values[8], values[9], values[6])
            scraper = Web_Scraping.process_tickets()
            scraper.get_page(url)
            cheapest = scraper.get_cheapest()
            response = f"The cheapest {values[2]} ticket found is: " + cheapest + "<br/>URL for the ticket: <a href='" + url + "'> Ticket </a>"
            session.clear()
            return response
        else:
            values = get_data(data_list)
            form_filler = Form_Automation.Form_filler()
            url = form_filler.single_ticket('https://www.thetrainline.com/', values[0], values[1], values[2], values[3].strftime("%d/%m/%y"), values[4], values[5], values[6])
            scraper = Web_Scraping.process_tickets()
            scraper.get_page(url)
            cheapest = scraper.get_cheapest()
            response = f"The cheapest {values[2]} ticket found is: " + cheapest + "<br/>URL for the ticket: <a href='" + url + "'> Ticket </a>"
            session.clear()
            return response
    else:
       response = "Please enter the " + check
       return response

def process_contingencies(sentence):
    data_list = ['Blockage', 'Origin', 'Destination', 'Intent']
    origin, destination, blockage, intent = NLP.processs_contingencies(sentence)
    if "Origin" not in session and origin == destination:
        destination = None
    data_values = [blockage, origin, destination, intent]
    add_to_session(data_list, data_values)
    check = check_session(data_list)
    if check is None:
        values = get_data(data_list)
        response = Disruption_Contingencies.respond(values)
        if response is not None:
            response = f"{values[3]} for {values[0]} blockage from {values[1]} to {values[2]} is: <br/>" + response
            session.clear()
            return response
        else:
            session.clear()
            return "I don't have the answer"
    else:
        response = "Please enter the: " + check
        return response 

def process_delay(sentence):
    data_list = ['Origin', 'Destination', 'Departure time', 'Departure delay', 'Arrival time', 'Month', 'Day']
    origin, destination, dep_time, dep_delay, arr_time, month, day = NLP.process_train_delay(sentence)
    if "Origin" not in session and origin == destination:
        destination = None
    if "Departure time" not in session and dep_time == arr_time:
        arr_time = None
    data_values = [origin, destination, dep_time, dep_delay, arr_time, month, day]
    add_to_session(data_list, data_values)
    check = check_session(data_list)
    if check is None:
        values = get_data(data_list)
        values[0] = Database_controller.get_station_name(values[0])[0][0]
        values[1] = Database_controller.get_station_name(values[1])[0][0]
        delay  = Delay_Prediction.predict_values("BEST_NN.joblib", values[0], values[1], values[2], values[3], values[4], values[5], values[6])
        response = "Your predicted delay is: " + str(int(round(delay[0]))) + " minutes"
        session.clear()
        return response
    else:
        response = "Please enter the: " + check
        return response
   
def process_training(sentence):
    train = session['train_sent']
    if 'Booking' in sentence:
        Database_controller.add_intent_sentences(train, 'B')
        session.clear()
        Reasoning.train_model()
        session['state'] = 'B'
        handle_intent(train)
    elif 'Contingencies' in  sentence:
        Database_controller.add_intent_sentences(train, 'C')
        session.clear()
        Reasoning.train_model()
        session['state'] = 'C'
        handle_intent(train)
    elif 'Delay' in sentence:
        Database_controller.add_intent_sentences(train, 'D')
        session.clear()
        Reasoning.train_model()
        session['state'] = 'D'
        handle_intent(train)
    elif 'Weather' in sentence:
        Database_controller.add_intent_sentences(train, 'W')
        session.clear()
        Reasoning.train_model()
        session['state'] = 'W'
        handle_intent(train)

    elif 'Casual' in sentence:
        session['state'] = "T_C"
        return "How should I respond to this sentence?"
    else:
        return "Invalid input!"
        
def process_weather(sentence):
    s, n = NLP.process_sentence(sentence)
    loc = NLP.retrieve_loc(s, n)
    if loc is not None:
        weather = Weather.get_weather(loc)
        if weather is not None:
            response = weather.get_detailed_status() + " in " + loc + "<br/> Temperature: " + str(weather.get_temperature(unit='celsius')['temp'])
            session.clear()
            return response
        else:
            return "Weather for " + loc + " not available"
    else:
        return "Please enter the location"

##################################################################################################
#                                        Database training
##################################################################################################
def train_conversation(response):
    sentence = session['train_sent']
    Database_controller.add_new_convo(sentence, response)
    session.clear()
    return "Training completed"


##################################################################################################
#                                        Handling states
##################################################################################################
def add_to_session(data_list, data_values):
     for i, data in enumerate(data_list):
        if data not in session:
            if data_values[i] is not None:
                session[data] = data_values[i]

def check_session(data_list):
    print(session)
    for data in data_list:
        if data not in session:
            return data
    return None

##################################################################################################
#                                        Helper functions
##################################################################################################
def handle_ticket_types(origin, destination, t_type, date, hour, minute, amount, data_list, data_list_return):
    if t_type is not None and 'Ticket Type' not in session:
        session['Ticket Type'] = t_type
    if 'Ticket Type' in session and session['Ticket Type'] == "return":
        if len(date) == 1 and 'Departure Date' not in session:
            dep_date = date[0]
            ret_date = None
        elif len(date) == 1 and 'Departure Date' in session:
            ret_date = date[0]
            dep_date = None
        elif len(date) == 2:
            dep_date = date[0]
            ret_date = date[1]
        else:
            dep_date = None
            ret_date = None
        if len(hour) == 1 and len(minute) == 1 and 'Departure Hour' not in session:
            dep_hour = hour[0]
            ret_hour = None
            dep_minute = minute[0]
            ret_min = None
        elif len(hour) == 1 and len(minute) == 1 and 'Departure Hour' in session:
            ret_hour = hour[0]
            dep_hour = None
            ret_min = minute[0]
            dep_minute = None
        elif len(hour) == 2 and len(minute) == 2:
            dep_hour = hour[0]
            ret_hour = hour[1]
            dep_minute = minute[0]
            ret_min = minute[1]
        else:
            hour = None
            ret_hour = None
            minute = None
            ret_min = None
        data_values = [origin, destination, t_type, dep_date, dep_hour, dep_minute, amount, ret_date, ret_hour, ret_min]
        add_to_session(data_list_return, data_values)
        check = check_session(data_list_return)
    else:
        if len(date) == 1:
            dep_date = date[0]
        else:
            dep_date = None
        if len(hour) == 1 and len(minute) == 1:
            dep_hour = hour[0]
            dep_minute = minute[0]
        else:
            dep_hour = None
            dep_minute = None
        data_values = [origin, destination, t_type, dep_date, dep_hour, dep_minute, amount]
        add_to_session(data_list, data_values)
        check = check_session(data_list)
    time  = ["Hour", "Minute", "Departure Hour", "Departure Minute"]
    ret_time = ["Return Hour", "Return Minute"]
    if check in time:
        check = "Departure Time"
    elif check in ret_time:
        check = "Return Time"
    return check

def get_data(data_list):
    values = []
    for data in data_list:
        values.append(session[data])
    return values

if __name__ == '__main__':
    app.run(debug = True)