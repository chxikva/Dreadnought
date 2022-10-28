from datetime import datetime
from main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_relationship = db.relationship('User', foreign_keys='UserData.user') # look into this
    user_id_relationship = db.relationship('User', foreign_keys='UserData.user_id') # look into this
    sex = db.Column(db.String(20), nullable=True)
    height = db.Column(db.String(3), nullable=True)
    weight = db.Column(db.Float(5), nullable=True)
    tdee = db.Column(db.String(5), nullable=True)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.user}', '{self.user_id}', '{self.date_updated}')"