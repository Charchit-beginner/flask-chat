from flask_wtf import FlaskForm, RecaptchaField 
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import *

class RegistrationForm(FlaskForm):
	username = StringField('Username',
						validators=[DataRequired(), Length(min=8, max=20)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password',
						validators=[DataRequired(), Length(min=8, max=60)])
	confirm_password = PasswordField('Confirm Password',
						validators=[DataRequired(), Length(min=8, max=60), EqualTo('password')])
	# recaptcha = RecaptchaField('Please complete the verification below to register')
	submit = SubmitField('Sign Up')

	
	def validate_username(self, username):
		user = Detail.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists.')

class LoginForm(FlaskForm):
    # Validate required fields from user for sign in
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    # recaptcha = RecaptchaField('Please complete the verification below to sign in') # Used to prevent bots brute force sign ins
    # remember = BooleanField("Remember Me")
    submit = SubmitField('Login')