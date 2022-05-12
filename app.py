# import libs
import jwt
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import flask_sqlalchemy
import Scripts.secrets_folder as secrets_folder
from flask_session import Session
import pymysql
from flask import Markup
from werkzeug.security import generate_password_hash, check_password_hash
from Scripts.config import db
from Scripts.database import *
from flask_mail import Mail, Message
from administration import create_key

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
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = secrets_folder.email
app.config['MAIL_PASSWORD'] = secrets_folder.emailPass
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SESSION_TYPE'] = 'sqlalchemy'


# initialise mail
mail = Mail(app)

# initialise db and create tables after initialising db
db.init_app(app=app)
with app.app_context():
    db.create_all()

# create db.py obj
db_function = db_fun()

# initialise session to use sqlalchemy
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)
with app.app_context():
    sess.app.session_interface.db.create_all()


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
            user_passwd = db.session.query(Users.passwd).filter_by(  # get user passwd from db based on username
                username=uname_email).first()

            if user_passwd == None:  # if statement to check if user_passwd is None
                user_passwd = db.session.query(  # get user password from db based on email
                    Users.passwd).filter_by(email=uname_email).first()

                uname_email = db.session.query(  # get user name from email
                    Users.username).filter_by(email=uname_email).first()
                uname_email = uname_email[0]

            session['USER'] = uname_email

            # set user_passwd var to passwd hash string
            user_passwd = user_passwd[0]

            # create a session into db

            # check if user inputted passwd is the same as in db
            check_passwd = check_password_hash(user_passwd, passwd)
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
        # get data from authentication table
        au = Authenticate.query.all()
        au_email = [au[x].email for x in range(len(au))]
        au_key = [au[x].key for x in range(len(au))]
        au_data = au_email + au_key
        # get data from form in post request and set it to var
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        cfmPasswd = generate_password_hash(
            request.form['cfmpasswd'], 'sha256', salt_length=8)
        email = request.form['email']
        id = db_function.create_uid()
        key = request.form['key']

        # get User info from users table
        users = Users.query.all()
        users_email = [users[x].email for x in range(len(users))]

        # get confirmation status from db
        au_confirm = Authenticate.query.filter_by(email=email).first()
        au_confirm = au_confirm.confirmation_status
        # if else to check if user has all prerequisite to sign up
        if email in au_data and key in au_data and au_confirm == "pending":
            # create new users obj
            new_user = Users(userId=id, username=username,
                             passwd=cfmPasswd, fname=fname, lname=lname, email=email)
            # if statement to check if sign up email is same as admin email therefore giving it admin status
            if email == secrets_folder.adminEmail:
                new_user = Users(userId=id, username=username,
                                 passwd=cfmPasswd, fname=fname, lname=lname, email=email, authority='admin')

            # get status from authentication table and change the content
            status_update = Authenticate.query.filter_by(email=email).first()
            status_update.confirmation_status = 'approved'
        elif email in users_email:
            # raise error
            error = 'Email is already in use'
            flash(Markup('<p style="color:red;">Email is already in use, <a href="/" style="text-decoration:underline; color:red;">Click me</a> to return to log in page to log in instead</p>'))
            return render_template('sign-up1.html')

        # try to add user and commit if not except error and refresh page and show error msg
        try:
            # add user obj into db
            db.session.add(new_user)
            db.session.commit()
            db.session.remove()
            return render_template('sign-up1.html', flash_message='True')
        except:
            error = 'There was an issue adding user'
            flash(Markup(error))
            return redirect('sign-up')

    return render_template('sign-up1.html', flash_message='False')


# forgot password page


@app.route('/forgot-passwd')
def sign_up2():
    return render_template('forgot-passwd.html')

# request key page


@app.route('/req-key', methods=['GET', 'POST'])
def req_key():
    # if statement to get post request data
    if request.method == "POST":
        cfm_email = request.form['cfm-email']
        id = db_function.create_eid()
        key = create_key.key_generator()

        # get user data from db
        user = Users.query.all()
        users_email = [user[x].email for x in range(len(user))]

        # get data from authentication email
        au = Authenticate.query.all()
        au_email = [au[x].email for x in range(len(au))]

        # check if email is inside user table
        if cfm_email in users_email:
            error = 'Email is already in use.'
            return render_template('req-key.html', error=error)

        # check if email is in authentication table
        if cfm_email in au_email:
            error = 'Key request is pending or has already been sent.'
            return render_template('req-key.html', error=error)

        # create new authentication obj
        authentication = Authenticate(uid=id, email=cfm_email, key=key)

        # if statement to determine is email has admin status or not than rewrite data into obj
        if cfm_email == secrets_folder.adminEmail:
            authentication = Authenticate(
                uid=id, email=cfm_email, key=key, confirmation_status='pending')

        # try and except to catch any error
        try:
            # add obj into db
            db.session.add(authentication)
            db.session.commit()
            db.session.remove()
            # flash text msg to page
            text = "<div class="'key-req-flash'"><h3>Key request successful</h3><p>You will receive an email containing the key to sign up. Request will take up to 15 minutes to 24 hours. <a href='/'>Click me</a> to go back to login page</P></div>"
            flash(Markup(text))
            return redirect('req-key')
        except:
            error = 'There was an error requesting key'
            return render_template('req-key.html', error=error)

    return render_template('req-key.html')

# administration page


@app.route('/administration', methods=['GET', 'POST'])
def administration():

    # get all waiting emails
    au = Authenticate.query.all()
    wait_email = [au[x].email for x in range(
        len(au)) if au[x].confirmation_status == 'waiting']

    if session.get('USER'):
        user = session['USER']
        user_status = db.session.query(
            Users.authority).filter_by(username=user).first()[0]

        if user_status == 'admin':
            return render_template('approval.html', emails=au)

    # if statement to get post request data
    if request.method == "POST":
        # get email and pass from form
        uname_email = request.form.get('uname_email')
        passwd = request.form.get('passwd')

        user_passwd = db.session.query(Users.passwd).filter_by(  # get user passwd from db based on username
            username=uname_email).first()
        if user_passwd == None:  # if statement to check if user_passwd is None
            user_passwd = db.session.query(  # get user password from db based on email
                Users.passwd).filter_by(email=uname_email).first()

            uname_email = db.session.query(  # get user name from email
                Users.username).filter_by(email=uname_email).first()
            uname_email = uname_email[0]

        session['USER'] = uname_email
        # set user_passwd var to passwd hash string
        user_passwd = user_passwd[0]
        # check if user inputted passwd is the same as in db
        check_passwd = check_password_hash(user_passwd, passwd)
        if check_passwd == True:
            return render_template('approval.html', emails=au)
        else:
            return render_template('approval.html', flash_message="False")

    return render_template('approval.html', flash_message="True")

# home page


@app.route('/my-folder')
def home():
    if session.get('USER'):
        user = session['USER']
        return render_template('my-folder.html', user=user)
    else:
        return render_template('my-folder.html')


@app.route('/logout')
def logout():
    # get user sess
    session.pop('USER', None)
    return redirect('/')


@app.route('/send_mail/<string:bool>/<int:id>')
def send_mail(bool, id):
    # get email and key
    status_update = Authenticate.query.filter_by(uid=id).first()
    email = status_update.email
    key = status_update.key
    # if else to check if admin approve or deny
    if bool == 'approve':
        # craft email and send it then redirect page
        msg = Message("Key Request", sender=secrets_folder.email,
                      recipients=[email])
        msg.html = f"<div style='text-align:center'><h3 style='color:rgb(5, 221, 5)'>Your request for unique key has been approved by the administrator</h3><p>Your unique key is : {key}</p><p>Enter this key when you signup</p></div>"
        mail.send(msg)
        print('Email sent')
        status_update.confirmation_status = 'approved'
        return redirect('/administration')
    elif bool == 'deny':
        # craft email and send it then redirect page
        msg = Message("Key Request", sender=secrets_folder.email,
                      recipients=[email])
        msg.html = "<div style='text-align:center'><h3 style='color:red'>Your request for unique key has been denied</h3></div>"
        mail.send(msg)
        print('Email sent')
        status_update.confirmation_status = 'Deny'
        return redirect('/administration')

    return redirect('/administration')

# function to check if any email waiting to be approve then send email to admin


# def admin_task():
    # get data from admin table from db
    # au = Authenticate.query
    # au = Authenticate.query.all()
    # print(au)
    # waiting_user = [au[x].uid for x in range(len(au))]

    # if waiting:
    #     token = jwt.encode({'exp': time() + 600},
    #                        secrets_folder.secret_key, algorithm='HS256')
    #     with app.app_context:
    #         msg = Message("User awaiting approval", sender=secrets_folder.email, recipients=[
    #                       secrets_folder.adminEmail], text_body=render_template('administration/approval.txt', token=token))
    #         mail.send(msg)
    #         print('Email sent')
    # else:
    #     pass


# apsched = BackgroundScheduler(daemon=True)
# apsched.add_job(admin_task, 'interval', minutes=1)
# apsched.start()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="8008")
    # admin_task()
