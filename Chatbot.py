from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify

app = Flask(__name__)
app.secret_key="AI_Chatbot"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message')
def process_message():
    return 0

if __name__ == '__main__':
    app.run(debug = True)