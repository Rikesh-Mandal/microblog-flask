from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

#for sending emails asynchronously, we need to create a new thread for each email. 
#This is because sending an email can take a long time, 
#and we don't want to block the main thread of the application while we're waiting for the email to be sent.
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#this function is used to send an email. 
# It takes the subject, sender, recipients, text body, and HTML body of the email as arguments.
#the Thread class is used to create a new thread that will run the send_async_email function.
def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()