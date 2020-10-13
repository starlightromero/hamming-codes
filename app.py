"""Import flask and SocketIO."""
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)


@socketio.on("message")
def handle_message(msg):
    """Send msg to everyone."""
    print(f"Message {msg}")
    send(msg, broadcast=True)


@app.route("/")
def home():
    """Render home page."""
    return render_template("home.pug")


@app.route("/welcome")
def welcome():
    """Render welcome page."""
    return render_template("welcome.pug")


if __name__ == "__main__":
    socketio.run(app)
