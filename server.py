from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


app.config['SECRET_KEY'] = 'cd337b99d301c53f0278a292fa12f5f40084d450'


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