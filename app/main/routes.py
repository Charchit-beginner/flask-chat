from  flask import Flask,Blueprint,render_template,session,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from app import socketio,db
from flask_socketio import emit, send
from app.models import *

main = Blueprint('main', __name__)



@socketio.on('connect')
def test_connect(auth):
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    emit('msg', data , broadcast=True , include_self=False)
    print(data)

@main.route("/")
@login_required
def index():
    return render_template("index.html") 

@main.route("/contacts")  
@login_required
def contacts():
    return render_template("users.html")