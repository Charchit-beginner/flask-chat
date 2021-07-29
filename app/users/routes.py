from  flask import Flask,Blueprint,render_template,session,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required
from app import socketio,db
from flask_socketio import emit, send
from app.users.forms import RegistrationForm,LoginForm
from app.models import *

users = Blueprint('users', __name__)


def test_connect(data):
    emit("regis",data,broadcast=True  ,namespace="/")


    
@users.route("/register",methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("It looks like You are already Registered","info")
        return redirect("/")
    form = RegistrationForm()
    if request.method=="POST" and form.validate_on_submit():
        user = Detail(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        socketio.on_event('register', test_connect(user.username),namespace="/")
        return redirect("/signin")
    return render_template("register.html",form=form)



@users.route("/signin",methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        flash("It looks like you are already logined to site","info")
        return redirect("/")
    form = LoginForm()
    if request.method=="POST" and form.validate_on_submit():
        user = Detail.query.filter_by(username=form.username.data,password=form.password.data).first()
        print(user)
        if user:
            login_user(user, remember=form.remember.data)
            flash("Logined successfully","success")
        else:
            flash("Unsuccessful Login. Please Try Again","danger")
        return redirect("/")

    return render_template("signin.html",form=form)

@users.route("/logout",methods=["POST"])
def logout():
    logout_user()
    flash("You successfully logged out","success")
    return redirect("/signin")


