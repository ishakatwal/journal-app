import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'home-is-where-the-heart-is'
    SQLALCHEMY_DATABASE_URI = "postgres://cdduxabtohsimk:b9f7c1f8e314d1369c26a93b3495c2b137ce5bf3aa3789364861884d850d5d64@ec2-174-129-227-51.compute-1.amazonaws.com:5432/d82l34813hjjtn"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_POST = int(os.environ.get('MAIL_POST') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['teglanigiro@gmail.com']
