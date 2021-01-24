from flask import Flask
from flask_moment import Moment
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler


journal_app = Flask(__name__)
journal_app.config.from_object(Config)
db = SQLAlchemy(journal_app)

login = LoginManager(journal_app)
login.login_view = 'login'
moment = Moment(journal_app)

from app import routes, models, errors
from app.models import User, Post


# Logic that handles emailing errors

if not journal_app.debug:
    if journal_app.config['MAIL_SERVER']:
        auth = None
        if journal_app.config['MAIL_USERNAME'] or journal_app.config['MAIL_PASSWORD']:
            secure = None
        if journal_app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (journal_app.config['MAIL_SERVER'], journal_app.config['MAIL_PORT']),
            fromaddr = 'no-reply@' + journal_app.config['MAIL_SERVER'],
            toaddrs = journal_app.config['ADMINS'], subject = 'Journal Failure',
            credentials = auth, secure = secure
            )
        mail_handler.setLevel(logging.ERROR)
        journal_app.logger.addHandler(mail_handler)

        #Log errors that are not major
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/journal.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s%(levelname)s:%(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        journal_app.logger.addHandler(file_handler)

        journal_app.logger.setLevel(logging.INFO)
        journal_app.logger.info('Journal initialization')
