from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import Scripts.secrets_folder as secrets_folder
import pymysql
import time
from werkzeug.security import generate_password_hash, check_password_hash
from Scripts.config import db
from Scripts.database import *

conn = "mysql+pymysql://%s:%s@%s:%s/%s" % (secrets_folder.dbuser, quote(
    secrets_folder.dbpass), secrets_folder.dbhost, secrets_folder.dbport, secrets_folder.dbname)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = conn
app.config['SECRET_KEY'] = secrets_folder.secret_key
# db = SQLAlchemy(app=app)
# db.init_app(app=app)

db.init_app(app=app)
with app.app_context():
    db.create_all()

# create db.py obj
db_function = db_fun()

# log in page


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('admin.html')

# sign up page 1


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    id = db_function.create_id()

    if request.method == "POST":
        req = request.form
        print(req)
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        # cfmPasswd = request.form['cfmpasswd']
        cfmPasswd = generate_password_hash(request.form['cfmpasswd'], 'sha256', salt_length=8)
        email = request.form['email']
        # id = db_function.create_id()
        print(cfmPasswd)
        
        new_user = Users(userId=id, username=username,
                         passwd=cfmPasswd, fname=fname, lname=lname, email=email)
        
        

        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.remove()
            return redirect('/')
        except:
            flash('There was an issue adding user')
            time.sleep(3)
            return redirect('/sign-up')
    else:
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
