# store route for website (login)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
 # don't store password in plain text 
 # hash functions have no inverse
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
# why we used UzerMixin in models.py
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        # get email and password
        email = request.form.get('email')
        password = request.form.get('password')

        # is user email valid
        # query the db 
        user = User.query.filter_by(email=email).first()
        if user:
            # check password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                # redirect user to home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again', category='error')
        else:
            flash('Email does not exist', category='error')


    return render_template("login.html", boolean=True)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # get info from form (email, info, and 2 passwords)
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # if info not valid, don't create a new user account
        # if valid then do create one
        # POST REQUEST
        user = User.query.filter_by(email=email).first()
        if user: 
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('first name must be grater than 2 characters', category='error')
        elif password1 != password2:
            flash('passwsords don\'t match', category="error")
        elif len(password1) < 7:
            flash('passwsords must be at least 7 charactres', category="error")
        else:
             # cretae a new user 
            new_user = User(email=email, first_name=first_name, 
                            password=generate_password_hash(password1, method='sha265'))
            # add user to database 
            db.session.add(new_user)
            db.session.commit() # commit to db
            login_user(user, remember=True)
            flash('Account created!', category="success")
            # redirect user to home page
            return redirect(url_for('views.home'))

    return render_template("login.html", boolean=True)