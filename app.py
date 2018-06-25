from flask import Flask, render_template, request

import backend.core as core

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extractmail', methods=['GET', 'POST'])
def extractmail():
    return render_template('extractmail.html')

@app.route('/sendmail')
def sendmail():
    return render_template('sendmail.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
