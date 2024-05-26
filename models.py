from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Favorite {self.city}, {self.country}>'