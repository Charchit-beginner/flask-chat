from app import db
from datetime import datetime
from app import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Detail.query.get(int(user_id))


class Detail(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(35),unique=True, nullable=False)
    email = db.Column(db.String(35),  nullable=False)
    password = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(15), default=datetime.now())
    user_message1 = db.relationship("Msg1", backref="owner1",cascade="all, delete, delete-orphan")
    user_message2 = db.relationship("Msg2", backref="owner2",cascade="all, delete, delete-orphan")


class Msg1(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    smsg = db.Column(db.String(1000))
    msg_type =  db.Column(db.String(3))
    susername = db.Column(db.String(20),db.ForeignKey("detail.username"))
    sget_user = db.Column(db.String(20))

class Msg2(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    rmsg = db.Column(db.String(1000))
    rmsg_type =  db.Column(db.String(3))
    rusername = db.Column(db.String(20),db.ForeignKey("detail.username"))
    rget_user = db.Column(db.String(20))


# from app import db,create_app
# from app.models import *
# app = create_app()
# with app.app_context():
#     db.create_all()