from app import db
from datetime import datetime


class Detail(db.Model):
    username = db.Column(db.String(35), primary_key = True, nullable=False)
    email = db.Column(db.String(35),  nullable=False)
    password = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(15), default=datetime.now())
    user_message = db.relationship("Message", backref="owner",cascade="all, delete, delete-orphan")

class Message(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	messages = db.Column(db.String(1000))
	username = db.Column(db.String(20),db.ForeignKey("detail.username"))
	get_user = db.Column(db.String(20))

