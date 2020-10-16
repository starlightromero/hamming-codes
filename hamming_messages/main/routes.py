from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from flask_socketio import send, join_room, leave_room
from hamming_messages import socketio, db
from hamming_messages.models import Message, User

main = Blueprint("main", __name__)

ROOMS = ["lounge", "news", "games", "coding"]


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


@socketio.on("usernameDisconnected")
def disconnect_username(username):
    """Get username and send message."""
    user = User.query.filter_by(username=username)
    print(username)
    user.sid = ""
    db.session.commit()


@socketio.on("join")
def on_join(data):
    """User joins a room."""
    username = data["username"]
    room = data["room"]
    join_room(room)
    send(
        {"message": f"{username} has joined {room}."},
        room=room,
    )


@socketio.on("leave")
def on_leave(data):
    """User leaves a room."""
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send({"message": f"{username} has left."}, room=room)


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
        "rooms": ROOMS,
    }
    return render_template("home.pug", **context)
