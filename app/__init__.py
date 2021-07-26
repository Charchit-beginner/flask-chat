from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager() 
login_manager.login_view = 'users.signin'
login_manager.login_message = "Login To Continue"
login_manager.login_message_category = 'info'

def create_app(config_class = Config):
	app.config.from_object(config_class)

	db.init_app(app)
	login_manager.init_app(app)


	from app.users.routes import users
	from app.main.routes import main

	app.register_blueprint(users)
	app.register_blueprint(main)

	socketio.init_app(app)

	return app

	