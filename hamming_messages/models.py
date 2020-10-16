from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt
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
    is_online = db.Column(db.Boolean, nullable=False, default=True)
    sid = db.Column(db.String(32), nullable=True)

    def set_password(self, password):
        """Set user's password as hash."""
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        """Check if given password matches hashed password."""
        return sha256_crypt.verify(password, self.password)


class Message(db.Model):
    """Message database class."""

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Room(db.Model):
    """Room database class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200), nullable=False)
