"""
The file contains the standard routes for authentication pages of our websites.
E.g. Login, Logout, Signup Page
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User # to access the database to insert data into it.import
from werkzeug.security import generate_password_hash, check_password_hash # apply encryption on password
from .import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) # method enables out python script to accept GET and POST request
def login():
    if request.method == 'POST':
        email= request.form.get('email')
        password = request.form.get('password')

        user= User.query.filter_by(email=email).first() # return the email equal to the entered email
        if user:
            if check_password_hash(user.password, password): #check the password hash and verify if it is correct
                flash('Logged in Successfully!!!', category= 'success')
                login_user(user, remember=True) # Remember the user that is logged in until session ends
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again', category= 'error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #Create a decorator to make sure we cannot access this unless we are logged in.
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email= request.form.get('email')
        first_name= request.form.get('firstName')
        password1= request.form.get('password1')
        password2= request.form.get('password2')

        user= User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category= 'error')
        elif len(email)<4:
            flash('Email must be greater than 4 character.', category= 'error')
        elif len(first_name)<2:
            flash('First name must be greater than 2 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match. Try re-entering', category= 'error')
        elif len(password1)<7:
            flash('Password must greater than or equal to', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) # Create a new user
            db.session.add(new_user) # Add new user to the database
            db.session.commit() # make commit to update the database
            login_user(user, remember=True)  # Login the user once they sign up
            flash('Account created!!', category='success')

            return redirect(url_for('views.home')) # Redirect the user to homepage after creating the new user

    return render_template("sign_up.html", user=current_user)