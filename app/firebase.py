import pyrebase
import os
# This file details with all firebase authentication
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
	"apiKey": "AIzaSyCax55fwQtaQnETvZbPqyQ4pJ5AferWO6s",
	"authDomain": "flask-chat-app-dc088.firebaseapp.com",
	"projectId": "flask-chat-app-dc088",
	"storageBucket": "flask-chat-app-dc088.appspot.com",
	"messagingSenderId": "434955273588",
	"appId": "1:434955273588:web:eafccf07b7a23743b4d821",
	"measurementId": "G-R17KS0MB9N",
	"databaseURL":"no"
}

firebase = pyrebase.initialize_app(CONFIG)
storage = firebase.storage()

auth = firebase.auth()
email = os.getenv("FIREBASE_USERNAME")
password = os.getenv("FIREBASE_PASSWORD")
firebase_user = auth.sign_in_with_email_and_password(email, password)