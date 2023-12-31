from flask import request, render_template
import requests
from app import app

@app.route('/')
@app.route('/home')
def reverie_test():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Logged into Reverie'
    else:
        return render_template ('login.html')