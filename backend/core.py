import re
import csv
from flask_mail import Mail, Message
from datetime import datetime
import smtplib
import dns.resolver

def email_find(name_is, csv_extract=True):
    email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
    try:
        if name_is[-4:].lower()  == '.txt' or name_is[-4:].lower() == '.csv':
            f = open(name_is,"r")
            contents = f.read()
            f.close()
            email_list = email_regex.findall(contents)
            current_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.csv'
            if csv_extract is True:
                with open(current_name, "w") as csv_file:
                        writer = csv.writer(csv_file)
                        for email in email_list:
                            writer.writerow([email])
                return True
            else:
                return email_list
        else:
            raise Exception("That's not a file we can read")
    except Exception as e:
        return e

def validate_recipient(email):
    fromAddress = 'yatharthrai16@ducic.ac.in'
    addressToVerify = str(email)

    # Get domain for DNS lookup
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])

    # MX record lookup
    records = dns.resolver.query(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)


    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()


    # Assume SMTP response 250 is success
    if code == 250:
    	return True
    else:
    	return False
