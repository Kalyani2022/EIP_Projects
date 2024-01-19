# import libraries
from datetime import date, datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import mysql.connector as mysql

# MySQL database connection details
db_config = {
   "host": "localhost",
   "user": "root",
   "password": "Kalyani2022",
   "database": "earthmaildb",
}

# Function to send an email with an attachment and save it to the database
def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_path):
   try:
        # Connect to the database
      connection = mysql.connect(**db_config)
      cursor = connection.cursor()

        # Read the attachment file and convert it to binary data
      with open(attachment_path, "rb") as fp:
         file_data = fp.read()

      now = datetime.now()
      date = now.strftime('%Y-%m-%d %H:%M:%S')


        # Insert the file data into the database
      insert_query = "INSERT INTO uploaded_files (date, filename, filedata) VALUES (%s, %s, %s)"
      values = (date, attachment_path, file_data)
      cursor.execute(insert_query, values)
      connection.commit()

        # Close the database connection
      connection.close()

        # Create a MIMEMultipart object
      message = MIMEMultipart()
      message["From"] = sender_email
      message["To"] = receiver_email
      message["Subject"] = subject

        # Add body to the email
      message.attach(MIMEText(body, "plain"))

        # Add the attachment to the email
      part = MIMEBase("application", "octet-stream")
      part.set_payload(file_data)
      encoders.encode_base64(part)
      part.add_header("Content-Disposition", f"attachment; filename= {attachment_path}")
      message.attach(part)

        # Connect to the SMTP server and send the email
      smtp_server = "smtp.gmail.com"
      smtp_port = 587
      with smtplib.SMTP(smtp_server, smtp_port) as server:
         server.starttls()
         server.login(sender_email, sender_password)
         server.sendmail(sender_email, receiver_email, message.as_string())

      print("Email sent successfully!")
   except Exception as e:
      print("Error:", e)

if __name__ == "__main__":
    # Set your email and SMTP server details here
   sender_email = "kal.ray111985@gmail.com"
   sender_password = 'bobexhjeuugaoqtc'
   receiver_email = "kalyani_bhattacharjee@rediffmail.com"
   subject = "Test Email with Attachment"
   body = "This is a test email with an attachment, which is successfully uploaded into database also ...."
   attachment_path = "E:\VSCode_2023\Project\Proj_earthInP_email_sent\project1\mf.csv"
    
    # Call the function to send the email with the attachment
   send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_path)
