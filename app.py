# import libs
from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import Scripts.secrets_folder as secrets_folder
import pymysql
import time
from werkzeug.security import generate_password_hash, check_password_hash
from Scripts.config import db
from Scripts.database import *

# create connection string
conn = "mysql+pymysql://%s:%s@%s:%s/%s" % (secrets_folder.dbuser, quote(
    secrets_folder.dbpass), secrets_folder.dbhost, secrets_folder.dbport, secrets_folder.dbname)

# initialise app
app = Flask(__name__)
# configure app configurations
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = conn
app.config['SECRET_KEY'] = secrets_folder.secret_key

# initialise db and create tables after initialising db
db.init_app(app=app)
with app.app_context():
    db.create_all()

# create db.py obj
db_function = db_fun()


# log in page
@app.route('/', methods=['POST', 'GET'])
def index():
    # if statement to check if post request is sent
    if request.method == "POST":
        # get data from form from post request
        uname_email = request.form['uname']
        passwd = request.form['passwd']
        
        # get user data from database
        user = Users.query.all()
        users_uname = [user[x].username for x in range(len(user))]
        users_email = [user[x].email for x in range(len(user))]
        users_uname_email = users_uname + users_email

        # check if username or email is in db
        if uname_email in users_uname_email:
            user_passwd = db.session.query(Users.passwd).filter_by( # get user passwd from db based on username 
                username=uname_email).first()
            if user_passwd == None: # if statement to check if user_passwd is None
                user_passwd = db.session.query( # get user password from db based on email
                    Users.passwd).filter_by(email=uname_email).first()
            user_passwd = user_passwd[0] # set user_passwd var to passwd hash string
            check_passwd = check_password_hash(user_passwd, passwd) # check if user inputted passwd is the same as in db
            if check_passwd == True:
                return redirect('/my-folder')
            else:
                error = 'Username, Email or Password is incorrect.'
                return render_template('admin.html', error=error)
        else:
            error = 'Username, Email or Password is incorrect.'
            return render_template('admin.html', error=error)

    return render_template('admin.html')

# sign up page 1


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    # if statement to check if post request is sent
    if request.method == "POST":
        # get data from form in post request and set it to var
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        cfmPasswd = generate_password_hash(
            request.form['cfmpasswd'], 'sha256', salt_length=8)
        email = request.form['email']
        id = db_function.create_id()

        # create new users obj
        new_user = Users(userId=id, username=username,
                         passwd=cfmPasswd, fname=fname, lname=lname, email=email)
        # try to add user and commit if not except error and refresh page and show error msg
        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.remove()
            return redirect('/')
        except:
            error = 'There was an issue adding user'
            return render_template('/sign-up', error=error)

    return render_template('sign-up1.html')


# sign up page 2


@app.route('/forgot-passwd')
def sign_up2():
    return render_template('forgot-passwd.html')

# home page


@app.route('/my-folder')
def home():
    return render_template('my-folder.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="8008")
