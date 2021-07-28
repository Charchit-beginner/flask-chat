from  flask import Flask,Blueprint,render_template,session,request,redirect,flash,Response,abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from app import socketio,db
from flask_socketio import emit, send, join_room, leave_room
from app.models import *
import jsonpickle

import functools
from flask_login import current_user
from flask_socketio import disconnect

users = {}
sids = {}

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

# jsonpickle.encode(user), mimetype='application/json' use this to send list

main = Blueprint('main', __name__)



@socketio.on('connect')
def test_connect(auth):
    print(users)
    sids[request.sid] = current_user.username
    users[current_user.username] = request.sid
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    del sids[request.sid]
    print('Client disconnected')

@socketio.on('message')
@authenticated_only
def handle_message(data):
    # if current_user.username == data[]
    # msg = Msg1(smsg=data["msg"],msg_type=,sget_user=data["user"],owner1=current_user)
    for i in sids:
        if sids[i] == data["user"] or sids[i] == current_user.username:
            print(data)
            emit('msg', {"msg":data["msg"],"user":current_user.username,"rec_user":data["user"]} , room=i)



 # users = {charchit:sfsfs,charhit1:sefegr}
 # sid = {sfsfs:charchit,srfegsf:charchit,sefegr:charchit1}

@main.route("/")  
@login_required
def index():
    users = Detail.query.filter(Detail.username!=current_user.username).all()
    return render_template("users.html",users=users)

@main.route("/chat/<user>")
@login_required
def chat(user):
    user = Detail.query.filter_by(username=user).first()
    return render_template("index.html",user=user) 

