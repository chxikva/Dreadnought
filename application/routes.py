import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm
from application.models import User, UserData
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash(f"Account created, you can now log in.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password.", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures/', picture_fn)
    # image is saved as a 0 byte image, find issue and fix it + resize it with Pillow
    """for picture_name in os.listdir('C:/Users/Nikoloz.Oboladze/Desktop/Dreadnought/application/static/profile_pictures'):
        while picture_fn == picture_name:
            new_random_hex = secrets.token_hex(8)
            _, new_f_ext = os.path.splitext(form_picture.filename)
            picture_fn = new_random_hex + new_f_ext
            new_picture_path = os.path.join(app.root_path, 'static/profile_pictures/', picture_fn)
            form_picture.save(new_picture_path)
        else:
            form_picture.save(picture_path)"""

    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)

    resized_image.save(picture_path)

    prev_picture = os.path.join(app.root_path, 'static/profile_pictures/', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        with app.app_context():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f"profile_pictures/{current_user.image_file}")
    return render_template('account.html', title='Account', image_file=image_file, form=form)