from math import floor
from flask import Blueprint, render_template, request, flash
from application.models import Post
from application.main.forms import CalorieCalculatorForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title="Home", posts=posts)


@main.route("/calculator", methods=['GET', 'POST'])
def calorie_calculator():
    form = CalorieCalculatorForm()
    if form.validate_on_submit():
        if form.gender.data == '1':
            tdee = (88.362 + (13.397 * form.weight.data) + (4.799 * form.height.data)
                    - (5.677 * form.age.data)) * float(form.activity.data)
            tdee_final = floor(tdee)
        else:
            tdee = (447.593 + (9.247 * form.weight.data) + (3.098 * form.height.data)
                    - (4.330 * form.age.data)) * float(form.activity.data)
            tdee_final = floor(tdee)
        flash(f"Calculated! Your TDEE is {tdee_final}", 'success')
    return render_template('calorie_calculator.html', title="Calorie Calculator", form=form)