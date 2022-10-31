from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cd337b99d301c53f0278a292fa12f5f40084d450'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin123@database-1.cb2rtyzdahf0.eu-central-1.rds.amazonaws.com:3306/test-db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from application import routes