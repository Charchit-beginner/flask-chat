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
    user_message1 = db.relationship("Message", backref="owner",cascade="all, delete, delete-orphan")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(1000))
    msg_type =  db.Column(db.String(5))
    username = db.Column(db.String(20),db.ForeignKey("detail.username"))
    get_user = db.Column(db.String(20))


# from app import db,create_app
# from app.models import *
# app = create_app()
# with app.app_context():
#     db.create_all()