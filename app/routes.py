from flask import request, render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm, SignUpForm
from app.models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')



#fix issue where it wont redirect you to HOMEPAGE when logging in to existing account.... 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username_or_email = form.email.data
        password = form.password.data

        user = None
        if '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid password', 'error')
        else:
            flash('User not found', 'error')

    return render_template('login.html', form=form)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(password)

        try:
            user = User(username, email, hashed_password)
            db.session.add(user)
            db.session.commit()

            print(f"User {user.username} created successfully")
            login_user(user)
            flash(f'Welcome to Reverie, {user.username}!', 'success')
            return redirect(url_for('home'))
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error during signup: {e}")
            if 'user_email_key' in str(e):
                flash('Email already exists. Please choose another.', 'error')
            else:
                flash('An error occurred. Please try again.', 'error')


    return render_template('signup.html', form=form)



@app.route('/logout')
@login_required
def logout():
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('login'))