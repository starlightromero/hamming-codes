from flask import Flask, render_template, Blueprint, request
from flask_login import login_required, current_user
from flask_socketio import send
from hamming_messages import socketio, db
from hamming_messages.models import Message, User

main = Blueprint("main", __name__)


@socketio.on("connect")
def connect_user():
    """Send message when user connects."""
    send("User has connected!")


@socketio.on("message")
def handle_message(data):
    """Send message to everyone."""
    send(data, broadcast=True)
    # message = Message(message=msg)
    # db.session.add(message)
    # send(msg, broadcast=True)


@main.route("/")
@login_required
def home():
    """Render home page."""
    messages = Message.query.all()
    users = User.query.all()
    context = {
        "messages": messages,
        "users": users,
        "sender": current_user.username,
    }
    return render_template("home.pug", **context)
