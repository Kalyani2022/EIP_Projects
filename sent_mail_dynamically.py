# iImport Libraries
import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename
from email import encoders

import pandas as pd
# import mysql.connector as sql
import pymysql as pysql

# table_name = 'customer_mail_info'

# Establish Database Connection
conn = pysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='*****',
    database='earthmaildb'
)

# Create cursor for fetching data from Database
cursor = conn.cursor()

query = f"select Mail_ID from customer_mail_info"
cursor.execute(query)
data = cursor.fetchall()

# Create Reciepient's List
recipients = []
for i in data:
    recipients.append(i[0])

# Declare Batch size
chunk = 100

# For testing Add 'test_mails' and create small batches for large number of Reciepient's list
test_emails = ['kalyanibhattacharjee@outlook.com', 'kalyani_bhattacharjee@rediffmail.com', 'priyasisb@gmail.com']
send_recipients = []
for i in range(0, len(recipients), chunk-2):
    chunk_recipients = recipients[i:i+(chunk-2)]
    chunk_recipients.insert((chunk-2) , test_emails[0])
    chunk_recipients.insert((chunk-1) , test_emails[1])
    send_recipients.append(chunk_recipients)

# Declare a dictionary for maximum attachments size per extension in bytes
attachment_size = {
    "txt" : 5000000,    # 5MB
    "doc" : 10000000,   # 10MB
    "docx" : 10000000,  # 10MB
    "pdf" : 10000000,   # 10MB
    "xlsx" : 10000000,  # 10MB
    "csv" : 10000000,  # 10MB
    "ppt"   : 10000000, # 10MB
    "pptx"  : 10000000, # 10MB
    "jpg" : 250000,     # 250KB
    "jpeg" : 250000,    # 250KB
    "png" : 250000      # 250KB
}
# total_attachment_size = 15000000   # 15MB

def send_mail(send_from, send_to, subject, body, file_path, app_password = '', server = '127.0.0.1', port = 25):
    assert isinstance(send_to, list)
    
    # Create a multipart message and set the headers
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['TO'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime= True)
    msg['Subject'] = subject

    # Add body to mail
    msg.attach(MIMEText(body, "plain"))

    # Extract the 'file_name' and 'file_extension' from the 'file_path'
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1][1:].lower()

    # Check if extension is allowed and get the maximum size for the extension
    max_attachment_size = attachment_size.get(file_extension)
    allowed_extension = ['.txt', '.doc', '.docx', '.pdf', '.xlsx', '.csv', '.ppt', '.pptx', '.jpg', '.jpeg', '.png']    
    if file_extension not in allowed_extension:
        print(f'Unsupported file extension : {file_extension}')
        return
        
    # Check the size of attached file    
    file_size = os.path.getsize(file_path)
    if file_size > max_attachment_size:
        print(f"File size exceed the maximum limit for extension {file_extension}, \nMaximum Size : {attachment_size} bytes")

    # Open the file in binary mode
    with open(file_path, 'rb') as fp:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(fp.read()),
                
    #Encode file in ASCII character to send by mail
    encoders.encode_base64(part)

    # Add header for attachment part
    part.add_header("Content-Disposition",f"attachment; filename= {file_name}",)

    # add attachment to msg        
    msg.attach(part)

    # convert message to string 
    text = msg.as_string()

    # LOgin to the SMTP server to send mail
    smtp = smtplib.SMTP(server, 587)
    smtp.starttls()
    smtp.login(send_from, app_password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if len(recipients)<11:
    l = len(recipients)
else:
    l = 11
for i in range(l):
    print(f"Iteration {i+1}")
    send_from = 'kal.ray111985@gmail.com'
    send_to = send_recipients.pop(i)
    subject = 'Long time no see !!!'
    body = "Please find the attach file"
    attachments = r"E:\\Dataset\\tss.csv"
        # r"C:\Users\KALYANI\Downloads\data_science_in_a_nutshell.jpg",
        # r"D:\Student_Library\MYSQL\Ebook_pdf\mssql.pdf",
        

    app_password = '*******'
    server = 'smtp.gmail.com'
    port = 587

    send_mail(send_from, send_to, subject, body, attachments, app_password, server, port)

    print(f"{i}-th chunks' mails are successfully sent...")

    # Introduce a 1-minute delay
    time.sleep(60)
