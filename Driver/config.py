import os

class Config:
    # App config
    SECRET_KEY = '086939e1532b75dc6d97c55b796d50e6'
    SQLALCHEMY_DATABASE_URI = "sqlite:///douh.db"

    # Reset mail login
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'douh.reset@gmail.com'
    MAIL_PASSWORD = 'dough35461157$'
