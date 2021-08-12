import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY')
	uri = os.getenv("DATABASE_URL")  # or other relevant config var
	if uri.startswith("postgres://"):
    	uri = uri.replace("postgres://", "postgresql://", 1)
	SQLALCHEMY_DATABASE_URI = uri
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG = True
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
	MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
	# RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
	# RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")