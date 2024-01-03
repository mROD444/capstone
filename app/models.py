from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app.extensions import db

db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    spotify_id = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"