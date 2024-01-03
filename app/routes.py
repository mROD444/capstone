from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from app import app
from app.models import User, db
from app.extensions import login_manager
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = '24f5696040ef42d6a4d1e90f7b55da4d'
SPOTIPY_CLIENT_SECRET = "7b3a085bf59e40d29d14646f81a5e24b"
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/spotify_callback'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read user-read-email')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/spotify_login')
def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



@app.route('/spotify_callback')
def spotify_callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    access_token = token_info['access_token']

    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.me()

    user = User.query.filter_by(spotify_id=user_info['id']).first()

    if not user:
        user = User(spotify_id=user_info['id'], username=user_info['display_name'])
        db.session.add(user)
        db.session.commit()

        login_user(user)

    flash('Successfully logged in with Spotify!', 'success')
    return redirect(url_for('home'))




@app.route('/logout')
@login_required
def logout():
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('login'))