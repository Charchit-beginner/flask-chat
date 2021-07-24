from  flask import Flask,Blueprint,render_template,session,request,redirect
from flask_sqlalchemy import SQLAlchemy
from app import socketio,db
from flask_socketio import emit, send
from app.forms import RegistrationForm
from app.models import *

view = Blueprint('views', __name__)


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

@view.route("/")
def index():
	return render_template("index.html")	
	
@view.route("/register",methods=["GET", "POST"])
def register():
	 form = RegistrationForm()
	 if request.method=="POST" and form.validate_on_submit():
	 	user = Detail(username=form.username.data,email=form.email.data,password=form.password.data)
	 	db.session.add(user)
	 	db.session.commit()
	 	return redirect("/signin")
	 return render_template("register.html",form=form)




@view.route("/signin")
def signin():
	return render_template("signin.html")



