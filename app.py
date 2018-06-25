from flask import Flask, render_template, request, url_for, redirect
from flask_mail import Mail, Message

import backend.core as core

app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
         x = request.form['name'].upper()
         return x
    return render_template('test.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extractmail', methods=['GET', 'POST'])
def extractmail():
    if request.method == 'POST':
        message = core.email_find(request.form['file_to_extract_from'])
        if message is True:
            return render_template('success.html', message="Extracted. Check the file folder for the data.")
        if message is not True:
            return render_template('failure.html', message=message)
    return render_template('extractmail.html')

@app.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    if request.method == 'POST':
        try:
            app.config.update(
            DEBUG=True,
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME = request.form['senderemail'],
            MAIL_PASSWORD = request.form['senderpassword']
            )
            mail = Mail(app)
            msg = Message(request.form['emailsubject'],
            sender=request.form['senderemail'],
    		recipients=request.form['recipientemail'].split())
            msg.body = request.form['emailcontent']
            mail.send(msg)
            return render_template('success.html', message="Email Sent!")
        except Exception as e:
            return render_template('failure.html', message=e)
    return render_template('sendmail.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
