from  flask import Flask,Blueprint,render_template,session,request,redirect,flash,Response,abort,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_,delete,select
from flask_login import current_user, login_required
from app import socketio,db
from flask_socketio import emit, send, join_room, leave_room
from app.models import *
from app.main.utils import *
import jsonpickle
import functools
from flask_login import current_user
from flask_socketio import disconnect
from app.firebase import storage,firebase_user

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
        sids[request.sid] = current_user.username
        emit('status', {'user': current_user.username,"status":"Online"},broadcast=True)
        current_user.status = "Online"
        db.session.commit()

@socketio.on('connected')
def get_id(data):
    if not current_user.is_anonymous:
        sids[request.sid] =  current_user.username + "user_contact"

@socketio.on('disconnect')
def test_disconnect():
    if not current_user.is_anonymous:
        cur_sid = sids[request.sid]
        del sids[request.sid]
        if not cur_sid.endswith("user_contact") and not cur_sid in [i for  i in sids.values()]:
            current_user.last_active =  datetime.utcnow()
            db.session.commit()

        if not cur_sid in [i for i in sids.values()] or (not cur_sid in [i for i in sids.values()] and cur_sid.endswith("user_contact")) :

            emit('status', {'user': current_user.username,"status":format_date()},broadcast=True)
            # if cur_sid in [i for  i in users.values()]:

            current_user.status = format_date()
            db.session.commit()
        print('Client disconnected')


# @socketio.on('disconnect',namespace="/")
# def dis():
#     print("dis user from here")

@socketio.on('typing')
@authenticated_only
def typing(data):
    if not current_user.is_anonymous and not userDeleted(data["user"]):
        for i in list(sids):
            if sids[i] == data["user"] or sids[i] == current_user.username or sids[i][:len(sids[i]) - 12] == data["user"] or sids[i][:len(sids[i]) - 12] == current_user.username:
                emit("type",{"typing":data["typing"],"user":current_user.username},room=i)
                    



@socketio.on('change')
@authenticated_only
def handle_change(data):
    if not current_user.is_anonymous:
        if current_user.username == data["current_user"]:
            for i in list(sids):
                if sids[i] == data["user"] or sids[i] == current_user.username or sids[i][:len(sids[i]) - 12] == data["user"] or sids[i][:len(sids[i]) - 12] == current_user.username:
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

@socketio.on('delete_all_msg')
@authenticated_only
def handle_message(data):
    if not current_user.is_anonymous:
        if current_user.username == data["current_user"]:
            emit("deleted_all")
            msgs = Message.query.filter_by(username=current_user.username,get_user=data["user"]).delete()
            db.session.commit()

@socketio.on('message')
@authenticated_only
def handle_message(data):
    if not current_user.is_anonymous  and not userDeleted(data["user"]):
        if len(data["msg"]) < 2000:
            rec_user = Detail.query.filter_by(username=data["user"]).first()
            msg = Message(msg=data["msg"],msg_type="right",get_user=data["user"],owner=current_user,time=datetime.utcnow())
            msg1 = Message(msg=data["msg"],msg_type="left",get_user=current_user.username,owner=rec_user,time=datetime.utcnow())        
            db.session.add(msg)
            db.session.add(msg1)
            db.session.flush()
            for i in list(sids):

                if sids[i] == data["user"] or sids[i] == current_user.username or sids[i][:len(sids[i]) - 12] == data["user"] or sids[i][:len(sids[i]) - 12] == current_user.username:
                    print(data)
                    emit('msg', {"msg":data["msg"],"user":current_user.username,"rec_user":rec_user.username,"status":rec_user.status,"date":format_date(),"id":msg.id} , room=i)
            db.session.commit()
            return "done!"
        else:
            emit("error_msg",{"error":"Limit of sending 2000 characters message exceeded"})


 # users = {charchit:sfsfs,charhit1:sefegr}
 # sid = {sfsfs:charchit,srfegsf:charchit,sefegr:charchit1}

@main.app_template_filter('get_img')
def get_img(img):
    return storage.child(img).get_url(firebase_user["idToken"]) if img != "default.jpg" else url_for('static',filename='images/default.jpg')




@main.route("/")  
@login_required
def index():
    users = Detail.query.filter(Detail.username!=current_user.username).all()
    # message = current_user.user_message1
    a,b= [],[]

    for  i in users:
        message = Message.query.filter_by(username=current_user.username,get_user=i.username).order_by(Message.id.desc()).first()

        msg = Message.query.filter(Message.username==current_user.username,Message.get_user==i.username,Message.time > current_user.last_active).all()
        d = Message.query.filter(Message.username==current_user.username,Message.get_user==i.username).all()
        b.append(msg)    
        a.append(message)
    return render_template("users.html",users=users,msg=a,unseen_msg=b)


@main.route("/chat/<user>")
@login_required
def chat(user):
    
    User = Detail.query.filter(Detail.username==user,Detail.username!=current_user.username).first()
    if not User:
        abort(404)
    message = Message.query.filter_by(username=current_user.username,get_user=User.username).order_by(Message.time).all()
    return render_template("index.html",user=User,message=message) 
