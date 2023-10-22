# mime stands for multipurpose internet mail extension
from email.mime import multipart 
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage # to accomodate image attachment
from email import encoders


username = '@gmail.com'
password = '' # the 16 digit character which we got from myaccounts.google.com


# defining a function to send a mail with attachment (picture)

def send_mail(uname,pwd,text="Object detected!!", subject="Cam capture",from_email= None,to_emails=None, html=None,attachment=None,):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart()
    msg['From'] = str(from_email)
    msg['To'] = ", ".join(str(to_emails))
    msg['Subject'] = subject

    # reading the image
    with open(attachment, 'rb') as f:
        img_data = f.read()

    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    image = MIMEImage(img_data, name=os.path.basename(attachment)) 
    msg.attach(image)
    msg_str = msg.as_string()
    
    # server side coding
    server = smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(uname, pwd)
    server.sendmail(from_email,list(to_emails),msg_str)
    server.quit() # quits the server


