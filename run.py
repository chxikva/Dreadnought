from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from main.forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cd337b99d301c53f0278a292fa12f5f40084d450'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin123@database-1.cb2rtyzdahf0.eu-central-1.rds.amazonaws.com:3306/test-db'
db = SQLAlchemy(app)


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


data = [
    {'date': '16 October, 2022',
     'name': 'nika',
     'sex': 'Male',
     'height': '180',
     'weight': '85',
     'age': '25',
     'tdee': '3250'
     },
    {'date': '16 October, 2022',
     'name': 'susan',
     'sex': 'Female',
     'height': '170',
     'weight': '60',
     'age': '25',
     'tdee': '2000'
    }
]


@app.route("/")
def home():
    return render_template('home.html', data=data, title="User Stats")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'nika@nika.ge' and form.password.data == 'password':
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password.", 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)