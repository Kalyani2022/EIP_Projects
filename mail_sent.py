import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from os.path import basename

# Sender:
#   id : kalyaniraybhatta@gmail.com
#   pwd : Kalyani@1985

# Receipient:
#   mailto : indrani.b2022@gmail.com

# gmail : smtp.gmail.com (port : 465, 587)
# yahoo : smtp.yahoo.com

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
    email_address = 'kal.ray111985@gmail.com'
    email_password = 'bobexhjeuugaoqtc'
    connection.login(email_address, email_password)
    connection.sendmail(from_addr= email_address, \
                        to_addrs= 'kalyani_bhattacharjee@rediffmail.com', \
                            msg= "subject : My first email sent via python script. \n\n email triggering \n\n for testing..")
    