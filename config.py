#just a config file
import os
from dotenv import load_dotenv


'''
__file__ returns the path to current python file
os.path.dirname - removes the filename and only returns the directory
abspath returns the absolute path
'''
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # makes sure the pymysql driver is used 
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('mysql://'):
        database_url = database_url.replace('mysql://', 
                                            'mysql+pymysql://',
                                              1)
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///' + os.path.join(basedir, 'db', 'app.db')

    # Email server configuration for sending error logs via email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['rikeshmandal26@gmail.com']

    #pagination configuration
    POSTS_PER_PAGE = 9

    # Internationalization (i18n) configuration
    # supported languages for the application
    LANGUAGES = ['en', 'es']  # English, Spanish, and German

    # elasticsearch config
    ELASTICSEARCH_URL=os.environ.get('ELASTICSEARCH_URL')
    ELASTICSEARCH_USERNAME=os.environ.get('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD=os.environ.get('ELASTICSEARCH_PASSWORD')
    ELASTICSEARCH_CA_CERT =os.environ.get('ELASTICSEARCH_CA_CERT')

    LIBRETRANSLATE_URL=os.environ.get('LIBRETRANSLATE_URL')

    # REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') == '1'