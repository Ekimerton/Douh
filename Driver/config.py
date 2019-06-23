import os

class Config:
    # App
    SECRET_KEY = os.environ['SECRET_KEY']

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

    # Reset mail login
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
