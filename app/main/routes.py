from  flask import Flask,Blueprint,render_template,session,request,redirect,flash,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from app import socketio,db
from flask_socketio import emit, send
from app.models import *
import jsonpickle

main = Blueprint('main', __name__)


@socketio.on('register')
def test_connect(auth):
    print(auth)
    user = Detail.query.filter_by(username=auth).first()
    emit("regis",jsonpickle.encode(user), mimetype='application/json',broadcast=True , include_self=False)

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
    users = Detail.query.filter(Detail.username!=current_user.username).all()
    return render_template("users.html",users=users)