import re
import csv
from flask_mail import Mail, Message
from datetime import datetime

def email_find(name_is):
    email_regex = re.compile(r'.+@\S+')
    try:
        if name_is[-3:] is not '.csv':
            raise Exception("That's not a .TXT file")
        f = open(name_is,"r")
        contents = f.read()
        f.close()
        email_list = email_regex.findall(contents)
        current_name = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.csv'
        with open(current_name, "w") as csv_file:
                writer = csv.writer(csv_file)
                for email in email_list:
                    writer.writerow([email])
        return True
    except Exception as e:
        return e

# Won't be used since this is already being done using flask_mail
def send_email(user=None, passw=None, msg=None, sendto=None):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, passw)
    server.sendmail(user, sendto, msg)
    server.quit()
