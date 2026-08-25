'''
the __init__.py is a package that can be imported
it executes and defines what symbols the package exposes to the outside world
'''

import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate  #for db migration
#sqlalchemy is an ORM - it allows high-level entities like classes, functions, methods to manage dbss
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment #for date and time formatting, flask_moment is a wrapper around moment.js, a JavaScript library for date and time formatting
from config import Config
 #for i18n and l10n, flask_babel is a wrapper around the Babel library, which provides tools for internationalization and localization in Python applications
from flask_babel import Babel, lazy_gettext as _l
from flask import request #request object is used to access the incoming request data, such as form data, query parameters, headers, etc.
from redis import Redis
import rq

def get_locale():
    # This function is used to determine the best match for the user's preferred language.
    # It uses the 'Accept-Language' header from the request to find the best match among the supported languages.
    return request.accept_languages.best_match(app.config['LANGUAGES'])
    


app = Flask(__name__) #creating instance of Flask 
app.config.from_object(Config) #reading and applying the config file

db = SQLAlchemy(app) #db object that represents the database
migrate = Migrate(app,db) #represents the db migration engine
login = LoginManager(app) #instance of the login manager which is provided by flask-login extension
login.login_view = 'login' #this line tells Flask-Login that the endpoint for the login view is 'login'.

# this line sets the message that will be flashed to the user when 
# they try to access a page that requires authentication, but they are not logged in. 
# The _l function is used for lazy translation of the message, 
# which means the translation will be done at the time the message is displayed, not when it is defined.
login.login_message = _l('Please log in to access this page.')

mail = Mail(app) #instance of the mail extension
moment = Moment(app) #instance of the moment extension
babel = Babel(app, locale_selector=get_locale) #instance of the babel extension
app.redis = Redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)


"""
Flask-Login provides a very useful feature that forces users to log in before they can view
certain pages of the application. If a user who is not logged in tries to view a protected page, 
Flask-Login will automatically redirect the user to the login form, and only redirect back to the 
page the user wanted to view after the login process is complete.
For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins. 
"""
login.login_view = 'login' 


# """Flask uses Python's logging package to write its logs, 
# and this package already has the ability to send logs by email. 
# All I need to do to get emails sent out on errors is to add a SMTPHandler 
# instance to the Flask logger object, which is app.logger:"""
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


# To enable a file based log another handler, 
# this time of type RotatingFileHandler, 
# needs to be attached to the application logger, similarly to the email handler.
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        """ensuring that the log files do not grow too large when the application runs for a long time.
        In this case I'm limiting the size of the log file to 10KB, and I'm keeping the last ten log files as backup."""
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)

        """format that includes the timestamp, the logging level, 
        the message and the source file and line number from where the log entry originated."""
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

        
        """To make the logging more useful, I'm also lowering the logging level to the INFO category, 
        both in the application logger and the file logger handler."""
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')








from app import routes, models, errors
