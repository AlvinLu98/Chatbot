from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, session
from random import randrange
import NLP, Reasoning, Database_controller, Delay_Prediction, Web_Scraping, Disruption_Contingencies, Form_Automation

app = Flask(__name__)
app.secret_key="AI_Chatbot"
intents = {
    'B' : 'Booking a ticket',
    'C' : 'Getting contingencies',
    'D' : 'Delay prediction',
    'N' : ''
}

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    sentence = request.form['message']
    print("Sentence: ", sentence)
    if "Quit" in sentence:
        session.clear()
        return jsonify(message = "Current running task ended, Goodbye!")
    response = Database_controller.get_chat_response(sentence)
    if len(response) == 0:
        if 'state' in session:
            response = handle_intent(sentence)
            return jsonify(message = response)
        else:
            intent, prob = Reasoning.predict(sentence)
            if(prob > 0.8):
                Database_controller.add_intent_sentences(sentence, intent)
                Reasoning.train_model()
                session['state'] = intent
                response = intents[intent] + "<br/>"
                response = response + handle_intent(sentence)
                return jsonify(message = response)
            else:
                session['state'] = "T"
                session['train_sent'] = sentence
                response = "I'm not sure what you are trying to do. Please enter either 'Booking', 'Contingencies, 'Delay' or 'Casual' to let me know what was your intent"
                return jsonify(message = response)
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
    elif session['state'] == 'T':
        response = process_training(sentence)
    elif session['state'] == 'T_C':
        response = train_conversation(sentence)
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
            url = form_filler.return_ticket('https://www.thetrainline.com/', values[0], values[1], values[2], values[3].strftime("%m/%d/%y"), values[4], values[5], values[6], values[7].strftime("%m/%d/%y"), values[8], values[9])
            scraper = Web_Scraping.process_tickets()
            scraper.get_page(url)
            cheapest = scraper.get_cheapest()
            response = f"The cheapest {values[2]} ticket found is: " + cheapest + "<br/>URL for the ticket: " + url
            session.clear()
            return response
        else:
            values = get_data(data_list)
            form_filler = Form_Automation.Form_filler()
            url = form_filler.single_ticket('https://www.thetrainline.com/', values[0], values[1], values[2], values[3].strftime("%m/%d/%y"), values[4], values[5], values[6])
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
        print(values)
        response = Disruption_Contingencies.respond(values)
        if response is not None:
            response = f"{values[3]} for {values[0]} blockage from {values[1]} to {values[2]} is: <br/>" + response
            session.clear()
            return response
        else:
            return "I don't have the answer"
    else:
        response = "Please enter the: " + check
        return response 

def process_delay(sentence):
    data_list = ['Origin', 'Destination', 'Departure time', 'Departure delay', 'Arrival time', 'Month', 'Day']
    origin, destination, dep_time, dep_delay, arr_time, month, day = NLP.process_train_delay(sentence)
    print(sentence, NLP.process_train_delay(sentence))
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
        print(values[0], values[1])
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
        return "Training completed"
    elif 'Contingencies' in  sentence:
        Database_controller.add_intent_sentences(train, 'C')
        session.clear()
        Reasoning.train_model()
        return "Training completed"
    elif 'Delay' in sentence:
        Database_controller.add_intent_sentences(train, 'D')
        session.clear()
        Reasoning.train_model()
        return "Training completed"
    elif 'Casual' in sentence:
        session['state'] = "T_C"
        return "How should I respond to this sentence?"
    else:
        return "Invalid input!"
        
def train_conversation(response):
    sentence = session['train_sent']
    Database_controller.add_new_convo(sentence, response)
    return "Training completed"

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

def handle_ticket_types(origin, destination, t_type, date, hour, minute, amount, data_list, data_list_return):
    if t_type is not None and 'Ticket Type' not in session:
        session['Ticket Type'] = t_type
    if 'Ticket Type' in session and session['Ticket Type'] == "return":
        if len(date) == 1 and 'Departure Date' not in session:
            date = date[0]
            ret_date = None
        elif len(date) == 1 and 'Departure Date' in session:
            ret_date = date[0]
            date = None
        elif len(date) == 2:
            date = date[0]
            ret_date = date[1]
        else:
            date = None
            ret_date = None
        if len(hour) == 1 and len(minute) == 1 and 'Departure Hour' not in session:
            hour = hour[0]
            ret_hour = None
            minute = minute[0]
            ret_min = None
        elif len(hour) == 1 and len(minute) == 1 and 'Departure Hour' in session:
            ret_hour = hour[0]
            hour = None
            ret_min = minute[0]
            minute = None
        elif len(hour) == 2 and len(minute) == 2:
            hour = hour[0]
            ret_hour = hour[1]
            minute = minute[0]
            ret_min = minute[1]
        else:
            hour = None
            ret_hour = None
            minute = None
            ret_min = None
        data_values = [origin, destination, t_type, date, hour, minute, amount, ret_date, ret_hour, ret_min]
        add_to_session(data_list_return, data_values)
        check = check_session(data_list_return)
    else:
        if len(date) == 1:
            date = date[0]
        else:
            date = None
        if len(hour) == 1 and len(minute) == 1:
            hour = hour[0]
            minute = minute[0]
        else:
            hour = None
            minute = None
        data_values = [origin, destination, t_type, date, hour, minute, amount]
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

def quit_process():
    return 0

if __name__ == '__main__':
    app.run(debug = True)