from flask import Flask, render_template, request, url_for, redirect
from flask_mail import Mail, Message, Attachment
import sys, os

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
        if message is not True:
            return render_template('failure.html', message=message)
        if message is True:
            return render_template('success.html', message="Extracted. Check the file folder for the data.")
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
            giant_list = []
            try:
                giant_list = core.email_find(request.form['emaillist'], csv_extract=False)
            except:
                pass
            f = open('Faulty_Email.txt', 'w')
            mail = Mail(app)
            if(request.form['recipientemail'] != None):
                giant_list = giant_list + request.form['recipientemail'].split()
            for recipe in giant_list:
                try:
                    msg = Message(request.form['emailsubject'],
                    sender="<"+request.form['sendertitle']+">",
            		recipients=[recipe])
                    # file_name = request.form['emailattachment']
                    # f = open(os.path.join(os.getcwd(), request.form['emailattachment']))
                    # with app.open_resource(request.form['emailattachment']) as fp:
                    #     print(fp.content_type, file=sys.stderr)
                    #     msg.attach(request.form['emailattachment'], fp.read())
                    msg.body = request.form['emailcontent']
                    print(request.form['emailattachment'], file=sys.stderr)
                    mail.send(msg)
                    msg_ = Message("National Innovation Foundation just opened the application",
                    sender="<NIF App Notification>",
            		recipients=["yatharthrai16@ducic.ac.in"])
                    msg_.body = "App has been opened. {} emails sent".format(len(giant_list))
                    mail.send(msg_)
                except Exception as e:
                    f.write(str(e) + "\n")
                    continue
            f.close()
            return render_template('success.html', message="Email(s) Sent!")
        except Exception as e:
            msg_ = Message("National Innovation Foundation Application Failed",
            sender="<NIF App Notification>",
    		recipients=["yatharthrai16@ducic.ac.in"])
            msg_.body = "Exception caught.{}".format(e)
            mail.send(msg_)
            return render_template('failure.html', message=e)
    return render_template('sendmail.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
