import os
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename
import time

import pandas as pd
import pymysql as pysql
from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'Kalyani2022',
    'database' : 'earthmaildb'
}

def get_db_connection_uploaded_files():
    conn = pysql.connect(**db_config)
    cursor = conn.cursor()

    query1 = "SELECT Mail_ID FROM customer_mail_info Limit 1000;"
    cursor.execute(query1)

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    print("Connection Successfully ... get_db_connection() --> works!!")

    return data


def sample_recipients():
    return  ['kalyanibhattacharjee@outlook.com', 'priyasisb@gmail.com']

def bilk_mails(data):

    recipients = []
    for i in data:
        recipients.append(i[0])

    chunk = 50
    test_emails = ['kalyanibhattacharjee@outlook.com', 'priyasisb@gmail.com']
    send_recipients = []

    for i in range(0, len(recipients), chunk-2):
        chunk_recipients = recipients[i:i+(chunk-2)]
        chunk_recipients.insert((chunk-2) , test_emails[0])
        chunk_recipients.insert((chunk-1) , test_emails[1])
        send_recipients.append(chunk_recipients)

    return send_recipients

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kal.ray111985@gmail.com'
app.config['MAIL_PASSWORD'] = 'bobexhjeuugaoqtc'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

mail = Mail(app)


@app.route("/")
def send_mail_to_all():
    return render_template('full.html')

@app.route("/full", methods= ["GET", "POST"])
def send_bulk_email(send_recipients):
    for i in range(len(send_recipients)):
        msg = Message('This is only for test mail..!', 
                      sender = 'kal.ray111985@gmail.com', 
                      recipients = send_recipients
                      )
        msg.body = "Hey guys, sending you this email from my Flask app, lmk if it works!!"
        mail.send(msg)
        print(f"{i}-th chunks' mails are successfully sent...")

        time.sleep(14400)       # Delay 4hrs
    return " All Messages, upto 1000 from starting, sent Successfully!"
# 
# @app.route("/")
# def index():
    # # msg = Message('This is only for test mail..!', sender = 'kal.ray111985@gmail.com', recipients = ['kalyani_bhattacharjee@rediffmail.com', 'kalyanibhattacharjee@outlook.com'])
    # msg.body = "Hey guys, sending you this email from my Flask app, lmk if it works!!"
    # mail.send(msg)
# 
    # return "Message sent!"
# 


if __name__ == '__main__':
    app.run(debug=True)




    # file_path = r"E:\\VScode\\flaskproject\\okay_code_list.txt"





    # file_name = os.path.basename(file_path)






    # try:

        # with app.open_resource(file_path, 'rb') as fp
        # with open(file_path, 'rb') as fp
            # part = MIMEBase("application", "octet-stream"
            # part.set_payload(fp.read())

            # encoders.encode_base64(part
            # # part.add_header("Content-Disposition",f"attachment; filename {basename(file_path)}")
            # msg.attach(file_path, "application/text", fp.read())
            # msg.attach(part, "application/text")
            # msg.attach(part)

    # except FileNotFoundError:
        # return "Error : Files not found"

    # mail.send(msg)



