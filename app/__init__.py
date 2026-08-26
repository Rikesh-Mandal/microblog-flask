'''
the __init__.py is a package that can be imported
it executes and defines what symbols the package exposes to the outside world
'''

import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy #sqlalchemy is an ORM - it allows high-level entities like classes, functions, methods to manage dbs
from flask_migrate import Migrate  #for db migration
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment #for date and time formatting, flask_moment is a wrapper around moment.js, a JavaScript library for date and time formatting
from flask_babel import Babel, lazy_gettext as _l #for i18n and l10n, flask_babel is a wrapper around the Babel library, which provides tools for internationalization and localization in Python applications
from redis import Redis
import rq
from config import Config


# This function is used to determine the best match for the user's preferred language.
# It uses the 'Accept-Language' header from the request to find the best match among the supported languages.
def get_locale():    
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    

db = SQLAlchemy() #db object that represents the database
migrate = Migrate() #represents the db migration engine
login = LoginManager() #instance of the login manager which is provided by flask-login extension
login.login_view = 'auth.login' #this line tells Flask-Login that the endpoint for the login view is 'login'.
login.login_message = _l('Please log in to access this page.')# The _l function is used for lazy translation of the message
mail = Mail() #instance of the mail extension
moment = Moment() #instance of the moment extension
babel = Babel() #instance of the babel extension


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)


    # """Flask uses Python's logging package to write its logs, 
    # and this package already has the ability to send logs by email. 
    # All I need to do to get emails sent out on errors is to add a SMTPHandler 
    # instance to the Flask logger object, which is app.logger:"""
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = ( app.config['MAIL_USERNAME'],
                         app.config['MAIL_PASSWORD'])
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

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

from app import models


