from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_socketio import SocketIO


app = Flask(__name__)
db = SQLAlchemy()
socketio = SocketIO()

def create_app(config_class = Config):
	app.config.from_object(config_class)

	db.init_app(app)

	from app.views import view

	app.register_blueprint(view)

	socketio.init_app(app)

	return app

	