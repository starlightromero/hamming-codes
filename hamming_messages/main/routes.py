from flask import Flask, render_template, Blueprint
from flask_socketio import send
from hamming_messages import socketio

main = Blueprint("main", __name__)


@socketio.on("message")
def handle_message(msg):
    """Send msg to everyone."""
    send(msg, broadcast=True)


@main.route("/")
def home():
    """Render home page."""
    messages = ["One", "Two", "Three"]
    context = {"messages": messages}
    return render_template("home.pug", **context)


@main.route("/welcome")
def welcome():
    """Render welcome page."""
    return render_template("welcome.pug")
