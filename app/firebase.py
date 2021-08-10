import pyrebase
import os
from app.firebase_config import CONFIG
# This file details with all firebase authentication


firebase = pyrebase.initialize_app(CONFIG)
storage = firebase.storage()


auth = firebase.auth()
email = "test1@gmail.com"
password = "1234567"
firebase_user = auth.sign_in_with_email_and_password(email, password)