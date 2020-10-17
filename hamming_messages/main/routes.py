from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import send, join_room, leave_room, emit
from reedsolo import RSCodec
from hamming_messages import socketio, db
from hamming_messages.models import Message, User, Room
from hamming_messages.main.forms import AddRoomForm
from hamming_messages.users.forms import UpdateAccountForm

main = Blueprint("main", __name__)


@socketio.on("userOnline")
def user_online(data):
    """User comes online."""
    username = data["username"]
    emit("userOnline", username, broadcast=True)


@socketio.on("userOffline")
def user_offline(data):
    """User goes offline."""
    username = data["username"]
    emit("userOffline", username, broadcast=True)


@socketio.on("disruptedMessage")
def handle_disrupted_message(data):
    """Send disrupted message to everyone."""
    # sender = User.query.filter_by(username=data["sender"]).first()
    # message = Message(message=data["message"], sender_id=sender.id)
    # db.session.add(message)
    # db.session.commit()
    # send(data, broadcast=True)


@socketio.on("message")
def handle_message(data):
    """Send message to everyone."""
    sender = User.query.filter_by(username=data["sender"]).first()
    message = Message(message=data["message"], sender_id=sender.id)
    db.session.add(message)
    db.session.commit()
    send(data, broadcast=True)


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
    add_room_form = AddRoomForm()
    update_account_form = UpdateAccountForm()
    rooms = Room.query.all()
    context = {
        "messages": messages,
        "users": users,
        "sender": current_user,
        "rooms": rooms,
        "add_room_form": add_room_form,
        "update_account_form": update_account_form,
    }
    return render_template("home.pug", **context)


@main.route("/room", methods=["PUT"])
@login_required
def add_room():
    """Add chat room to database."""
    name = request.json.get("name")
    description = request.json.get("description")
    if name and description:
        room = Room(name=name, description=description)
        db.session.add(room)
        db.session.commit()
        return (room.name), 201
    return (""), 404


@main.route("/room", methods=["DELETE"])
@login_required
def delete_room():
    """Delete chat room and remove from database."""
    name = request.json.get("name")
    if name:
        room = Room.query.filter_by(name=name).first_or_404()
        db.session.delete(room)
        db.session.commit()
        return (room.name), 200
    return (""), 404
