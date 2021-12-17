from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(36), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, default=datetime.now(pytz.timezone('US/Central')))
    anonymous = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_username(self):
        if self.anonymous:
            return 'Anonymous'
        else:
            return self.author.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))