from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import send, join_room, leave_room, emit
from reedsolo import RSCodec
from hamming_messages import socketio, db
from hamming_messages.models import Message, User, Room
from hamming_messages.main.forms import AddRoomForm
from hamming_messages.users.forms import UpdateAccountForm

main = Blueprint("main", __name__)


#                               HELPER FUNCTIONS


def distrupt_message(message):
    """Distrupt a given message."""
    length = len(message)
    rsc = RSCodec(length)
    b = bytearray()
    b.extend(map(ord, message))
    b_arr = rsc.encode(b)
    disrupted_arr = bytearray()
    count = 0
    for a in b_arr:
        if count < length and count % 3 == 0:
            a = 88
        disrupted_arr.append(a)
        count += 1
    disrupted_string = disrupted_arr[0:length].decode("utf-8")
    return (disrupted_string, disrupted_arr, length)


def decode_message(disrupted_arr, length):
    """Decode disrupted bytearray into string."""
    rsc = RSCodec(length)
    decoded_arr = rsc.decode(disrupted_arr)
    decoded_string = decoded_arr[0].decode("utf-8")
    return decoded_string


#                                   SOCKETS


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
    disrupted_string, disrupted_arr, length = distrupt_message(
        data["message"]
    )
    sender = User.query.filter_by(username=data["sender"]).first()
    room = Room.query.filter_by(name=data["room"]).first()
    message = Message(
        message=disrupted_string,
        disrupted_arr=disrupted_arr,
        length=length,
        sender_id=sender.id,
        room=room,
    )
    db.session.add(message)
    db.session.commit()
    send(
        {
            "message": disrupted_string,
            "sender": sender.username,
            "disrupted": True,
        },
        broadcast=True,
    )


# @socketio.on("decodeMessage")
# def handle_decode_message(data):
#     """Decode message and send to everyone."""
#     message = Message.query.filter_by(message=data["message"]).first()
#     decoded_string = decode_message(message.disrupted_arr, message.length)
#     decoded_message = Message(
#         message=decoded_string,
#         sender=message.sender,
#         room=message.room,
#     )
#     db.session.add(decoded_message)
#     db.session.commit()
#     send(
#         {
#             "message": decoded_message.message,
#             "sender": decoded_message.sender.username,
#         },
#         broadcast=True,
#     )


@socketio.on("message")
def handle_message(data):
    """Send message to everyone."""
    sender = User.query.filter_by(username=data["sender"]).first()
    message = Message(
        message=data["message"], sender_id=sender.id, room_id=sender.room_id
    )
    db.session.add(message)
    db.session.commit()
    send(data, broadcast=True)


@socketio.on("join")
def on_join(data):
    """User joins a room."""
    username = data["username"]
    room = data["room"]
    join_room(room)
    user = User.query.filter_by(username=username).first_or_404()
    current_room = Room.query.filter_by(name=room).first()
    try:
        user.room_id = current_room.id
        db.session.commit()
        send(
            {"message": f"{username} has joined {room}."},
            room=room,
        )
    except AttributeError:
        print("There are no chat rooms.")


@socketio.on("leave")
def on_leave(data):
    """User leaves a room."""
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send({"message": f"{username} has left."}, room=room)


#                               ROUTES


@main.route("/")
@main.route("/chat")
@login_required
def home():
    """Render home page."""
    messages = Message.query.all()
    users = User.query.all()
    add_room_form = AddRoomForm()
    update_account_form = UpdateAccountForm()
    rooms = Room.query.all()
    current_room = None
    try:
        current_room = current_user.room
    except AttributeError:
        current_room = Room.query.first()
    current_room_name = None
    try:
        current_room_name = current_room.name
    except AttributeError:
        current_room_name = None
    context = {
        "messages": messages,
        "users": users,
        "sender": current_user,
        "rooms": rooms,
        "current_room": current_room_name,
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


@main.route("/<room>/messages", methods=["GET"])
@login_required
def get_messages(room):
    """Get all messages for a given room."""
    current_room = Room.query.filter_by(name=room).first()
    try:
        messages = Message.query.filter_by(room_id=current_room.id).all()
        message_dict = {}
        for message in messages:
            message_dict.update({message.id: message.todict()})
        return message_dict, 200
    except AttributeError:
        print("There are no messages.")
        return "", 200


@main.route("/messages/<distupted_message>", methods=["GET"])
def handle_decode_message(distupted_message):
    """Decode given message."""
    message = Message.query.filter_by(message=distupted_message).first()
    decoded_string = decode_message(message.disrupted_arr, message.length)
    return decoded_string, 200
