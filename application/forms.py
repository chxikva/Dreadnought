from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, \
    SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from application.models import User


# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=3, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('Username taken. Please choose different username.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('Email taken. Please choose different email.')
#
#
# class LoginForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')
#
#
# class UpdateAccountForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=3, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#     gender = RadioField('Gender', validators=[Optional()], choices=[('Male', 'Male'), ('Female', 'Female')])
#     age = IntegerField('Age', validators=[Optional()])
#     height = IntegerField('Height', validators=[Optional()])
#     weight = FloatField('Weight', validators=[Optional()])
#     activity = SelectField('Activity Level', validators=[Optional()],
#                            choices=[(1.2, 'Sedentary - Little or No Exercise, Moderate Walking, Desk Job (Away from Home)'),
#                                     (1.375, 'Slightly Active - Exercise or Light Sports 1 to 3 Days a Week, Light Jogging or Walking 3 to 4 Days a Week'),
#                                     (1.55, 'Moderately Active - Physical Work, Exercise, or Sports 4 to 5 Days a Week, Construction Laborer'),
#                                     (1.75, 'Very Active - Heavy Physical Work, Exercise, or Sports 6 to 7 Days a Week, Hard Laborer'),
#                                     (1.9, 'Extremely Active - Very Heavy Physical Work or Exercise Every Day, Professional/Olympic Athlete')])
#     submit = SubmitField('Update')
#
#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('Username taken. Please choose different username.')
#
#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('Email taken. Please choose different email.')


# class CalorieCalculatorForm(FlaskForm):
#     gender = RadioField('Gender', validators=[DataRequired()], choices=[(1, 'Male'), (2, 'Female')])
#     age = IntegerField('Age', validators=[DataRequired()])
#     height = IntegerField('Height', validators=[DataRequired()])
#     weight = FloatField('Weight', validators=[DataRequired()])
#     activity = SelectField('Activity Level', validators=[DataRequired()],
#                            choices=[
#                                (1.2, 'Sedentary - Little or No Exercise, Moderate Walking, Desk Job (Away from Home)'),
#                                (1.375, 'Slightly Active - Exercise or Light Sports 1 to 3 Days a Week, Light Jogging or Walking 3 to 4 Days a Week'),
#                                (1.55, 'Moderately Active - Physical Work, Exercise, or Sports 4 to 5 Days a Week, Construction Laborer'),
#                                (1.75, 'Very Active - Heavy Physical Work, Exercise, or Sports 6 to 7 Days a Week, Hard Laborer'),
#                                (1.9, 'Extremely Active - Very Heavy Physical Work or Exercise Every Day, Professional/Olympic Athlete')])
#     submit = SubmitField('Calculate')


# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     content = TextAreaField('Content', validators=[DataRequired()])
#     submit = SubmitField('Post')


# class RequestResetForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError('There is no account with that email.')
#
#
# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')
