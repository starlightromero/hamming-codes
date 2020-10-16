from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from flask_socketio import send
from hamming_messages import socketio, db
from hamming_messages.models import Message, User

main = Blueprint("main", __name__)


@socketio.on("message")
def handle_message(data):
    """Send message to everyone."""
    sender = User.query.filter_by(username=data["sender"]).first()
    message = Message(message=data["message"], sender_id=sender.id)
    db.session.add(message)
    db.session.commit()
    send(data, broadcast=True)


@socketio.on("usernameConnected")
def connect_username(username):
    """Get username and send message."""
    user = User.query.filter_by(username=username)
    user.sid = request.sid
    db.session.commit()
    send(f"{username} has connected!", broadcast=True)


@socketio.on("usernameDisconnected")
def disconnect_username(username):
    """Get username and send message."""
    user = User.query.filter_by(username=username)
    print(username)
    user.sid = ""
    db.session.commit()
    send(f"{username} has disconnected!", broadcast=True)


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
