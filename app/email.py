from threading import Thread
from flask_mail import Message
from flask import render_template
from app import mail
from app import app
from flask_babel import _

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
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(app.get_current_object(), msg)).start()
    Thread(target=send_async_email, args=(app, msg)).start()

#this function is used to send a password reset email to a user.
#checks if the user exists and then generates a token for the user.
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
