from  flask import Flask,Blueprint,render_template,session,request,redirect,flash,Response,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_,delete,select
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
    if not current_user.is_anonymous:
        print(sids)
        sids[request.sid] = current_user.username
        users[current_user.username] = request.sid
        emit('status', {'user': current_user.username,"status":"Online"},broadcast=True)
        current_user.status = "Online"
        db.session.commit()

@socketio.on('disconnect')
def test_disconnect():
    if not current_user.is_anonymous:
        cur_sid = sids[request.sid]
        del sids[request.sid]
        if not cur_sid in [i for i in sids.values()]:
            emit('status', {'user': current_user.username,"status":str(datetime.now())[5:16]},broadcast=True)
            current_user.status = str(datetime.now())[5:16]
            db.session.commit()
        print('Client disconnected')


@socketio.on('typing')
@authenticated_only
def typing(data):
    print(data)
    if not current_user.is_anonymous:
        for i in list(sids):
            if sids[i] == data["user"] or sids[i] == current_user.username:
                emit("type",{"typing":data["typing"],"user":current_user.username},room=i)
                    



@socketio.on('change')
@authenticated_only
def handle_change(data):
    print(data, data["type"] == "cur_d_all")
    if not current_user.is_anonymous:
        if current_user.username == data["current_user"]:
            for i in list(sids):
                if sids[i] == data["user"] or sids[i] == current_user.username:
                    emit("change_ok",{"user":current_user.username,"id":data["id"],"type":data["type"]},room=i)            
            if data["type"] == "user_d":
                msg = Message.query.filter_by(id=data["id"],msg_type="left",username=current_user.username,get_user=data["user"]).first()
                db.session.delete(msg)
            elif data["type"] == "cur_d_me":
                msg = Message.query.filter_by(id=data["id"],msg_type="right",username=current_user.username,get_user=data["user"]).first()
                print(msg)
                db.session.delete(msg)
            if data["type"] == "cur_d_all":
                msg1 = db.session.query(Message).filter(
                    and_(or_(Message.id==data["id"],Message.id==int(data["id"])+1),or_(Message.username == current_user.username,and_(Message.username == data["user"],Message.get_user == current_user.username,Message.msg_type == "left")))).delete()
                
        db.session.commit()
        return "removed"

@socketio.on('message')
@authenticated_only
def handle_message(data):
    if not current_user.is_anonymous:
        rec_user = Detail.query.filter_by(username=data["user"]).first()
        msg = Message(msg=data["msg"],msg_type="right",get_user=data["user"],owner=current_user,time=str(datetime.now())[5:16])
        msg1 = Message(msg=data["msg"],msg_type="left",get_user=current_user.username,owner=rec_user,time=str(datetime.now())[5:16])        
        db.session.add(msg)
        db.session.add(msg1)
        db.session.flush()
        for i in list(sids):
            if sids[i] == data["user"] or sids[i] == current_user.username:
                print(data)
                emit('msg', {"msg":data["msg"],"user":current_user.username,"rec_user":data["user"],"date":str(datetime.now())[5:16],"id":msg.id} , room=i)
        db.session.commit()
        return "done!"


 # users = {charchit:sfsfs,charhit1:sefegr}
 # sid = {sfsfs:charchit,srfegsf:charchit,sefegr:charchit1}



@main.route("/")  
@login_required
def index():
    users = Detail.query.filter(Detail.username!=current_user.username).all()
    # message = current_user.user_message1
    a= []
    for  i in users:
        message = Message.query.filter_by(username=current_user.username,get_user=i.username).order_by(Message.id.desc()).first()
        a.append(message)
    return render_template("users.html",users=users,msg=a)


@main.route("/chat/<user>")
@login_required
def chat(user):
    user = Detail.query.filter_by(username=user).first()
    message = Message.query.filter_by(username=current_user.username,get_user=user.username).all()
    return render_template("index.html",user=user,message=message) 
