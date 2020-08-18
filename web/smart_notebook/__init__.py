import os
import secrets
from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", secret_key)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///site.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['TRANSLATOR_KEY'] = os.getenv("TRANSLATOR_KEY")
app.config['TRANSLATOR_REGION'] = os.getenv("TRANSLATOR_REGION")
app.config['TRANSLATOR_TEXT_ENDPOINT'] = os.getenv("TRANSLATOR_TEXT_ENDPOINT",
                                                   "https://api.cognitive.microsofttranslator.com/")

mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from smart_notebook import routes
