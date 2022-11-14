from application.models import *
from application import app, db

engine = app.config['SQLALCHEMY_DATABASE_URI']

with app.app_context():
    db.create_all()