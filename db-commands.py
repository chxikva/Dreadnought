from server import *

user_1_data = UserData(user='runsonlentils', user_id='1', sex='Male')
user_1 = User(username='nikatest', email='nika@gmail.com', password='test123@')

engine = app.config['SQLALCHEMY_DATABASE_URI']

with app.app_context():
    db.create_all()