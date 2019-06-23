from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from Driver import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    ingredients = db.relationship('Ingredient', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(50), nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    num_of_people = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients_raw = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    preperation = db.Column(db.Text, nullable=False)
    cooking = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric, nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    unit = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.description}', '{self.date}')"
