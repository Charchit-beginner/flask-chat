# Flask Chatting App
### A fully functional Chatting app made with flask-socketIO.
#### Live - https://charchit-chatapp.herokuapp.com/

# Steps to use app locally
### Prerequisites
- Python 3 on linux and windows (mac not tested)
- Flask (virtual environment or globally)
- Install all the requirements using `pip install -r requirements.txt`
- Firebase account
- Pushy account
### Run the app
#### 1. configure the env file (explained below).
#### 2. Comment the line `SQLALCHEMY_DATABASE_URI = uri` and uncomment `SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"` in config.py
#### 3. Comment the whole script tag in the layout.html at line 4
#### 4. delete the migration folder and open the terminal in the root folder and run 
- `flask db init` - initializing flask-migrate
- `flask db migrate` - create migration 
- `flask db upgrade` - make the database
- `python run.py` - run the app 
- Visit this [link](http://127.0.0.1:5000) to see the website

# Make .env file
```.env
DATABASE_URL= "heroku database url" # leave this if not using heroku
FIREBASE_USERNAME="test1@gmail.com" 
FIREBASE_PASSWORD="1234567" 
EMAIL_PASSWORD="Email_password" 
EMAIL_USERNAME="Email" 
SECRET_KEY="e72f434e77d246b6a55b2c9a8c2077" 
# You can get all these from firebase console
API_KEY="Firebase_api_key" 
AUTH_DOMAIN="firebase_auth_domain" 
PROJECT_ID="firebase_project_id" 
STORAGE_BUCKET="firebase_bucket_link" 
MESSAGE_SENDER_ID="612879935941" 
APP_ID="firebase_app_id" 
MEASUREMENT_ID="Ms_id"
```

# Technologies used in the app
- python3 
  - flask as backend
  - flask-sqlalchemy as orm
  - flask-socketIO 
  - pyrebase4 for connecting to fireabase to save user image
  - other third party modules like wtforms, flask-Migrate, flask_login
- Used Sqlite (for development) and postgresql (for production)
- HTML, CSS, JS, JQUERY, bootstrap
- PushySdk for push notification

# Features
- Full authentication system 
  - Email verification through otp
  - Forgot password and reset email
- Add profile pic
- fully responsive
- Messages saved in the database
- Delete chat for everyone
- Delete chat for me
- block user
- User Status - (like idle, online, offline, typing)
- Shows number of unseen message on the users page
- Notification tune on recieving message
- Push Notification facility for one device

### Note - The app is still under development. So you may see some bugs. Please contact me when you come across any.

## Contributing
Contributions are highly appreciated. If you want to contribute first fork the repo. And then make your changes. Now make a pull request stating the changes you made. I will review it and if it looks good to I will accept it and merge.

## Contacting
You can contact `charchit#8198` on discord or email at charchit.dahiya@gmail.com or even chat with me on the same app.
