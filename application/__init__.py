from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import boto3
from application.config import Config

load_dotenv()
# app = Flask(__name__)
# app.config.from_object(Config)
AWS_REGION = "eu-central-1"
ses = boto3.client('ses', region_name=AWS_REGION)
# app.config['SECRET_KEY'] = 'cd337b99d301c53f0278a292fa12f5f40084d450'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin123@database-1.cb2rtyzdahf0.eu-central-1.rds.amazonaws.com:3306/test-db'
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# from application.users.routes import users
# from application.posts.routes import posts
# from application.main.routes import main
#
# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from application.users.routes import users
    from application.posts.routes import posts
    from application.main.routes import main
    from application.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

#from application import routes