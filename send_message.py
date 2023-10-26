import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587  
SMTP_USERNAME = "shatviksweta7@gmail.com" 
SMTP_PASSWORD = "kmdl yiwd cxnr flyb"

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT phone_number, passcode FROM students")
rows = cursor.fetchall()

# Connect to the SMTP server
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    for row in rows:
        email, passcode = row

        # Create a message
        message = MIMEMultipart()
        message['From'] = SMTP_USERNAME
        message['To'] = email
        message['Subject'] = "Your Passcode"

        # Add the passcode to the message body
        body = f"Your passcode is {passcode}"
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(SMTP_USERNAME, email, message.as_string())

conn.close()
