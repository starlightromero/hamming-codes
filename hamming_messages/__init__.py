"""Import flask and SocketIO."""
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hamming_messages.config import Config

cors = CORS()
db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.login_view = "users.signin"
login_manager.session_protection = "strong"


def create_app(config_class=Config):
    """Resuable app function."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")

    db.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from hamming_messages.main.routes import main
    from hamming_messages.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    with app.app_context():
        db.create_all()

    return app
