from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Driver.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from Driver.users.routes import users
from Driver.posts.routes import posts
from Driver.main.routes import main
from Driver.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
