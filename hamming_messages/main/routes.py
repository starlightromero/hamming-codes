from flask import Flask, render_template, Blueprint
from flask_login import login_required
from flask_socketio import send
from hamming_messages import socketio, db
from hamming_messages.models import Message

main = Blueprint("main", __name__)


@socketio.on("message")
def handle_message(msg):
    """Send msg to everyone."""
    message = Message(message=msg)
    db.session.add(message)
    db.session.commit()
    send(msg, broadcast=True)


@main.route("/")
@login_required
def home():
    """Render home page."""
    messages = Message.query.all()
    context = {"messages": messages}
    return render_template("home.pug", **context)
