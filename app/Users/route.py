from flask import render_template,Blueprint
from app.Users.forms import LoginForm

users = Blueprint('users', __name__)



@users.route('/index')
def index():
    # user = {'username': 'Miguel'}
    return render_template('index.html', title='Home')

@users.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@users.route('/register')
def register():
    form = LoginForm()
    return render_template('register.html', title='Sign In', form=form)