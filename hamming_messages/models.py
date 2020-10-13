from datetime import datetime
from flask_login import UserMixin
from hamming_messages import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Get current logged in user."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User database class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=True)
    messages = db.relationship("Message", backref="sender", lazy=True)


class Message(db.Model):
    """Message database class."""

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
