from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from flaskext.markdown import Markdown

# App config
app = Flask(__name__)
app.config['SECRET_KEY'] = '086939e1532b75dc6d97c55b796d50e6'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///douh.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# Reset mail login
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'douh.reset@gmail.com'
app.config['MAIL_PASSWORD'] = 'dough35461157$'
mail = Mail(app)

from Driver.users.routes import users
from Driver.posts.routes import posts
from Driver.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
