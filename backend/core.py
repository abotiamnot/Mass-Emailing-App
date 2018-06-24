import re
import csv
import smtplib

def email_find(name, extract_name=None, csv_write=True):
    if extract_name is None:
        extract_name = "Email_List.csv"
    else:
        extract_name = extract_name + '.csv'
    email_regex = re.compile(r'.+@\S+')
    f = open(name,"r")
    contents = f.read()
    f.close()
    email_list = email_regex.findall(contents)
    with open(extract_name, "w") as csv_file:
            writer = csv.writer(csv_file)
            for email in email_list:
                writer.writerow([email])

def send_email(user=None, passw=None, msg=None, sendto=None):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, passw)
    server.sendmail(user, sendto, msg)
    server.quit()
