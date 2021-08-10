import pyrebase
import os
from app.firebase_config import CONFIG
# This file details with all firebase authentication
from dotenv import load_dotenv

load_dotenv()

firebase = pyrebase.initialize_app(CONFIG)
storage = firebase.storage()

auth = firebase.auth()
email = os.getenv("FIREBASE_USERNAME")
password = os.getenv("FIREBASE_PASSWORD")
firebase_user = auth.sign_in_with_email_and_password(email, password)