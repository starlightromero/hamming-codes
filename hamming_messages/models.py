"""Import libraries."""
from datetime import datetime
from flask import url_for, current_app
from flask_login import UserMixin
from flask_mail import Message as MailMessage
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hamming_messages import db, login_manager, mail


@login_manager.user_loader
def load_user(user_id):
    """Get current logged in user."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User database class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    messages = db.relationship("Message", backref="sender", lazy=True)
    is_online = db.Column(db.Boolean, nullable=False, default=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))

    def __repr__(self):
        """User returns username and room name."""
        return f"User('{self.username}', '{self.room.name}')"

    def set_password(self, password):
        """Set user's password as hash."""
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        """Check if given password matches hashed password."""
        return sha256_crypt.verify(password, self.password)

    def get_reset_token(self, expires_sec=900):
        """Generate user token to reset password."""
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    def send_reset_email(self):
        """Send password reset email."""
        token = self.get_reset_token()
        msg = MailMessage(
            "Password Reset Request",
            recipients=[self.email],
        )
        msg.body = f"""To reset your password, visit the following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
"""
        mail.send(msg)

    @staticmethod
    def verify_reset_token(token):
        """Verify given token."""
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except ValueError:
            return None
        return User.query.get(user_id)


class Message(db.Model):
    """Message database class."""

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    disrupted_arr = db.Column(db.BigInteger)
    length = db.Column(db.Integer)

    def __repr__(self):
        """Message returns sender username and room name."""
        return f"Message('{self.sender.username}', '{self.room.name}')"

    def todict(self):
        """Turn room into dictionary."""
        disrupted = False
        if self.disrupted_arr:
            disrupted = True
        return {
            "id": self.id,
            "message": self.message,
            "sender": self.sender.username,
            "room": self.room.name,
            "disrupted": disrupted,
        }


class Room(db.Model):
    """Room database class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    users = db.relationship("User", backref="room", lazy=True)
    messages = db.relationship("Message", backref="room", lazy=True)
