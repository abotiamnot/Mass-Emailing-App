from flask import Flask, render_template, request, url_for, redirect
from flask_mail import Mail, Message, Attachment
import sys, os, mimetypes

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
    # Did the user click the SUBMIT button?
    f_ = open('Completed_Steps.txt', 'w')
    if request.method == 'POST':
        try:
                # Let's initialize what is required!
                app.config.update(DEBUG=True,
                                  MAIL_SERVER='smtp.gmail.com',
                                  MAIL_PORT=465,
                                  MAIL_USE_SSL=True,
                                  MAIL_USERNAME = request.form['senderemail'],
                                  MAIL_PASSWORD = request.form['senderpassword'])
                f_.write("Initialized!" + "\n")
                # Let's create a Mail Object with the settings!
                mail = Mail(app)
                placeholder_ = core.email_find(request.form['emaillist'], csv_extract=False)
                f_.write("Passed to be extracted" + "\n")
                if(type(placeholder_) == list):
                    a = placeholder_
                else:
                    a = []
                try :
                    b = request.form['recipientemail'].split()
                except:
                    b = []
                giant_list = a + b
                final_list = []
                f_.write(str(giant_list))
                f_.write("\n")
                #Let's find the faulty emails!
                f = open('Faulty_Email.txt', 'w')
                for recipe in giant_list:
                    try:
                        criteria = core.validate_recipient(recipe)
                        f_.write("{} = {} \n".format(recipe, criteria))
                    except Exception as e:
                        f_.write("Exception caught {} = {} \n".format(e, recipe))
                        continue
                    if criteria == True:
                        final_list = final_list + [recipe]
                    else:
                        f.write(recipe + "\n")
                        continue
                f.close()
                # Let's mail the working emails!
                f_.write(str(final_list))
                f_.write("\n")
                for working_email in final_list:
                    msg = Message(request.form['emailsubject'],
                                  sender="<"+request.form['sendertitle']+">",
                                  recipients=[working_email])
                    msg.body = request.form['emailcontent']
                    if request.form['emailattachment']:
                        path_attach = os.path.join(os.getcwd(), request.form['emailattachment'])
                        with app.open_resource(path_attach) as fp:
                            mimetype = mimetypes.guess_type(path_attach)
                            msg.attach(request.form['emailattachment'], mimetype[0], fp.read())
                    mail.send(msg)
                f_.close()
                # Inform me at least, will ya?
                msg_ = Message("National Innovation Foundation just opened the application",
                               sender="<NIF App Notification>",
                               recipients=["yatharthrai16@ducic.ac.in"])
                msg_.body = "App has been opened. {} emails sent".format(len(final_list))
                mail.send(msg_)
                return render_template('success.html', message="Email(s) Sent!")
        #Exception caught, mail it to me.
        except Exception as e:
                msg_ = Message("National Innovation Foundation Application Failed",
                sender="<NIF App Notification>",
        		recipients=["yatharthrai16@ducic.ac.in"])
                msg_.body = "Exception caught.{} / {} / {}".format(e, a, b)
                mail.send(msg_)
                return render_template('failure.html', message=e)
    return render_template('sendmail.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
