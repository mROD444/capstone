from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b3a085bf59e40d29d14646f81a5e24b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jypblkbe:KOoZtW8sJQyulxBJ9yPt101RPBmex0RC@drona.db.elephantsql.com/jypblkbe'

db.init_app(app)
migrate = Migrate(app,db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    from app import routes

