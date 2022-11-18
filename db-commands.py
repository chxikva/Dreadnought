from application.models import *
from application import app, db

with app.app_context():
    user = User.query.filter_by(email="didi10akademia@gmail.com").first()

print(user.email)