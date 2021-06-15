import smtplib, ssl
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f = open('EMAIL_ADDRESS.json')
data = json.load(f)
sender = data['sender']
receiver = data['receiver']
password = data['password']
f.close()

smtp_server = "smtp.gmail.com"
port = 587
context = ssl.create_default_context()

def send_msg(message):
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender, password)
        msg = MIMEText(message, 'plain')
        msg['From']='Dimoski Database'
        msg['To']=receiver
        msg['Subject']=''
        msg = msg.as_string()
        server.sendmail(sender,receiver,msg)
        del msg
    except Exception as e:
        print(e)
    finally:
        server.quit()

#send_msg("Test of my system - hope it works")
