"""Import flask and SocketIO."""
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from hamming_messages.config import Config

db = SQLAlchemy()
socketio = SocketIO()
cors = CORS()


def create_app(config_class=Config):
    """Resuable app function."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    cors.init_app(app)

    from hamming_messages.main.routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
