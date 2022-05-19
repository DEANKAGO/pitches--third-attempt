from flask import render_template,Blueprint,url_for, flash, redirect, request
from app.Users.forms import LoginForm,Register,ResetPassword,UpdateAccountForm,VerifyOtp,ForgotPassword
from app import  db, bcrypt,mail
from flask_mail import  Message
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Otp
import random
import math

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash('Your Account Has been Created! You are now able to login  in', 'success')
        return redirect(url_for('users.login'))
    return render_template('signin.html', title='Register', form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username.title()} !! ', 'success')
           
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/forgot/password',methods=['POST','GET'])
def forgot_password():
    form=ForgotPassword()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        token=generate_token(6)
        otp=Otp(otp=token,user_id=user.id)
        db.session.add(otp)
        db.session.commit()
        if user:    
            msg=Message("Hello",sender="apollolibrary99@gmail.com",recipients=[user.email])
            msg.body = token
            mail.send(msg)
            flash('We have sent you an email with instructions to reset your password')
            return redirect(url_for('users.verify_otp',userid=user.id))

    return render_template('forgot_password.html',form=form)

@users.route('/otp-verify/<userid>',methods=['POST', 'GET'])
def verify_otp(userid):
    form = VerifyOtp()
    user=User.query.filter_by(id=userid).first()
    token=Otp.query.filter_by(user_id=userid).first()
    
    if form.validate_on_submit():

        if form.otp.data != token.otp:
            flash('InCorrect otp')
        else:
            flash('Correct otp')
            u=db.session.get(Otp,1)
            db.session.delete(u)
            db.session.commit()
            return redirect(url_for('users.reset',userid=user.id))

    return render_template('otp_verification.html',form=form)


def generate_token(length):
    digits = [i for i in range(0, 10)]

    token=""
    for i in range(length):
        index=math.floor(random.random()*10)
        token+=str(digits[index])
    return token

@users.route('/reset_password/<userid>',methods=['POST','GET'])
def reset(userid):
    form=ResetPassword()
    user=User.query.filter_by(id=userid).first()

    if form.validate_on_submit():
        if user.password != form.password.data:
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('Old and new password cannot be the same')
    return render_template('reset_password.html',form=form)

@users.route('/receipts', methods=['POST', 'GET'])
@login_required
def create():
    form = receipts()
    if form.validate_on_submit():
        receipts = receipts(title=form.title.data,
                      content=form.content.data, user_id=current_user.id,category=form.category.data)
        db.session.add(receipts)
        db.session.commit()
        flash('your request was successful')
        return redirect(url_for('main.home'))
    return render_template('create.html', form=form, )


# @users.route('/index')
# def index():
#     # user = {'username': 'Miguel'}
#     return render_template('index.html', title='Home')

# @users.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)

# @users.route('/register')
# def register():
#     form = LoginForm()
#     return render_template('register.html', title='Sign In', form=form)

@users.route('/account',methods=['POST', 'GET'])
@login_required
def account():
    """
    """
    
    user = User.query.filter_by(id=current_user.id)
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture=save_picture(form.picture.data)
            current_user.image_file=picture
             
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.id=form.id.data

        db.session.commit()
        flash('Your Account Has been updated!','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':

        form.username.data=current_user.username
        form.email.data=current_user.email
    
    image_file= url_for('static',filename='profiles/'+current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form, user = User)