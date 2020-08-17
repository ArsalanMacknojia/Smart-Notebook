import logging
from smart_notebook import db
from datetime import datetime
from flask_login import UserMixin
from smart_notebook import login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

LOGGER = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------------------------------User-------------------------------------------------------------


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_image = db.Column(db.String(40), default='default.jpg')
    notes = db.relationship('Note', backref='author', lazy=True, foreign_keys='Note.user_id')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            LOGGER.error("Password reset token verification failed", e)
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_image}')"


# -----------------------------------------------------Note-------------------------------------------------------------


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.author}', '{self.title}', '{self.date_posted}')"

    def as_dict(self):
        return {'title': self.title}
