from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, FloatField,\
    SelectField, SubmitField
from wtforms.validators import DataRequired


class CalorieCalculatorForm(FlaskForm):
    gender = RadioField('Gender', validators=[DataRequired()], choices=[(1, 'Male'), (2, 'Female')])
    age = IntegerField('Age', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    activity = SelectField('Activity Level', validators=[DataRequired()],
                           choices=[
                               (1.2, 'Sedentary - Little or No Exercise, Moderate Walking, Desk Job (Away from Home)'),
                               (1.375, 'Slightly Active - Exercise or Light Sports 1 to 3 Days a Week, Light Jogging or Walking 3 to 4 Days a Week'),
                               (1.55, 'Moderately Active - Physical Work, Exercise, or Sports 4 to 5 Days a Week, Construction Laborer'),
                               (1.75, 'Very Active - Heavy Physical Work, Exercise, or Sports 6 to 7 Days a Week, Hard Laborer'),
                               (1.9, 'Extremely Active - Very Heavy Physical Work or Exercise Every Day, Professional/Olympic Athlete')])
    submit = SubmitField('Calculate')