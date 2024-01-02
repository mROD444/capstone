from flask import request, render_template, redirect, url_for
from app import app
from app.forms import LoginForm, SignUpForm

REGISTERED_USERS = {
    'mel@test.com': {
        'username': 'first',
        'password': 'test'
    }
}

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data

        if email in REGISTERED_USERS and REGISTERED_USERS[email]['password'] == password:
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        REGISTERED_USERS[email] = {
            'username': username,
            'password': password
        }
        return f'Welcome to Reverie, {username}! Your journey begins now.'
    else:
        return render_template('signup.html', form=form)
