from math import floor
from datetime import *
from flask import current_app, Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from application import ses, db, bcrypt
from application.models import User, Post
from application.users.forms import RegistrationForm, LoginForm,\
    UpdateAccountForm, ResetPasswordForm, RequestResetForm
from application.users.utils import save_picture
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        with current_app.app_context():
            db.session.add(user)
            db.session.commit()
        flash(f"Account created, you can now log in.", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registration', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please check email and password.", 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    tdee = 0
    form = UpdateAccountForm()
    if form.validate_on_submit():
        with current_app.app_context():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.gender = form.gender.data
            current_user.age = form.age.data
            current_user.height = form.height.data
            current_user.weight = form.weight.data
            current_user.activity = form.activity.data
            user = User.query.filter_by(email=current_user.email).first()
            user.date_updated = datetime.now()
            db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.gender.data = current_user.gender
        form.age.data = current_user.age
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        form.activity.data = current_user.activity
        if form.gender.data == 'Male':
            const_kcal = 88.362
            weight_kcal = 13.397 * float(form.weight.data)
            height_kcal = 4.799 * int(form.height.data)
            age_kcal = 5.677 * int(form.age.data)
            activity_kcal = float(form.activity.data)
            tdee = floor((const_kcal + weight_kcal + height_kcal - age_kcal) * activity_kcal)
        elif form.gender.data == 'Female':
            const_kcal = 447.593
            weight_kcal = 9.247 * float(form.weight.data)
            height_kcal = 3.098 * int(form.height.data)
            age_kcal = 4.330 * int(form.age.data)
            activity_kcal = float(form.activity.data)
            tdee = floor((const_kcal + weight_kcal + height_kcal - age_kcal) * activity_kcal)
    image_file = url_for('static', filename=f"profile_pictures/{current_user.image_file}")
    return render_template('account.html', title='Account', image_file=image_file, form=form, tdee=tdee)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_user_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        SENDER = "Nika's Website <nika.oboladze@gmail.com>"
        SUBJECT = "Password Reset Request"
        RECIPIENT = user.email
        BODY_TEXT = f"Hello, to reset your password, please visit the following link:\n" \
                    f"{url_for('users.reset_token', token=token, _external=True)}\n" \
                    f"If you did not make this request then ignore this email."
        BODY_HTML = f"""
        <html>
        <head></head>
        <body>
        <h4>Hello, to reset your password, please visit the following link:</h4>
        <p>{url_for('users.reset_token', token=token, _external=True)}</p>
        <small>If you did not make this request then ignore this email.</small>
        </body>
        </html>
        """
        CHARSET = "utf-8"
        msg = MIMEMultipart('mixed')
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = RECIPIENT
        msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
        htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        msg_body.attach(textpart)
        msg_body.attach(htmlpart)
        msg.attach(msg_body)
        ses.send_raw_email(Source=SENDER,
                           Destinations=[RECIPIENT],
                           RawMessage={'Data': msg.as_string()}
                           )
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_user_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        with current_app.app_context():
            user.password = hashed_password
            db.session.commit()
        flash(f"Your password has been updated.", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)