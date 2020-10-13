from flask import Flask, render_template, Blueprint
from hamming_messages import db
from hamming_messages.models import User

users = Blueprint("users", __name__)


@users.route("/welcome")
def welcome():
    """Render welcome page."""
    return render_template("welcome.pug")
