# import libs
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import Scripts.secrets_folder as secrets_folder
import pymysql
from flask import Markup
from werkzeug.security import generate_password_hash, check_password_hash
from Scripts.config import db
from Scripts.database import *
from flask_mail import Mail, Message
from administation import create_key

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

# initialise mail
mail = Mail(app)

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
            user_passwd = db.session.query(Users.passwd).filter_by(  # get user passwd from db based on username
                username=uname_email).first()
            if user_passwd == None:  # if statement to check if user_passwd is None
                user_passwd = db.session.query(  # get user password from db based on email
                    Users.passwd).filter_by(email=uname_email).first()
            # set user_passwd var to passwd hash string
            user_passwd = user_passwd[0]
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
            flash('True')
            return redirect('/')
        except:
            error = 'There was an issue adding user'
            flash(Markup(error))
            return redirect('sign-up')

    return render_template('sign-up1.html')


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
    # msg = Message("hi", sender=secrets_folder.email, recipients=['furiousdragon93@gmail.com'])
    # msg.body = "Hi this is a test for auto email from python"
    # mail.send(msg)
    # print(msg)
    # print('msg sent')
    # return redirect('/')
    return render_template('req-key.html')

# administration page


@app.route('/administration', methods=['GET', 'POST'])
def administration():
    # if statement to get post request data
    if request.method == "POST":
        # get email and pass from form
        uname_email = request.form.get('uname_email')
        passwd = request.form.get('passwd')

        # get all waiting emails
        au = Authenticate.query.all()
        wait_email = [au[x].email for x in range(len(au)) if au[x].confirmation_status == 'waiting']

        user_passwd = db.session.query(Users.passwd).filter_by(  # get user passwd from db based on username
            username=uname_email).first()
        if user_passwd == None:  # if statement to check if user_passwd is None
            user_passwd = db.session.query(  # get user password from db based on email
                Users.passwd).filter_by(email=uname_email).first()
        # set user_passwd var to passwd hash string
        user_passwd = user_passwd[0]
        # check if user inputted passwd is the same as in db
        check_passwd = check_password_hash(user_passwd, passwd)
        if check_passwd == True:
            return render_template('approval.html', emails=wait_email)
        else:
            return render_template('approval.html', flash_message="False")

    return render_template('approval.html', flash_message="True")

# home page


@app.route('/my-folder')
def home():
    return render_template('my-folder.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="8008")
