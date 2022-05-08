from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import secrets_folder
import pymysql
import time


# conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
#     secrets_folder.dbuser, secrets_folder.dbpass, secrets_folder.dbhost, secrets_folder.dbname)
# conn = f"mysql+pymysql:///{secrets_folder.dbuser}:{secrets_folder.dbpass}@{secrets_folder.dbhost}/{secrets_folder.dbname}"
conn = "mysql+pymysql://%s:%s@%s:%s/%s" % (secrets_folder.dbuser, secrets_folder.dbpass, secrets_folder.dbhost, secrets_folder.dbport, secrets_folder.dbname)
# conn = "mysql://root:B@sketba1l@192.168.86.31:3306/storagesystem"

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = conn
app.config['SECRET_KEY'] = secrets_folder.secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app=app)


class Users(db.Model):
    userId = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(50))
    passwd = db.Column(db.String(25))
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(225))



# log in page


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('admin.html')

# sign up page 1


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        req = request.form
        print(req)

        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        cfmPasswd = request.form['cfmpasswd']
        email = request.form['email']
        new_user = Users(userId='a1', username=username,
                         passwd=cfmPasswd, fname=fname, lname=lname, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
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
    # app.run(debug=True, host='0.0.0.0', port="8008")
    print(conn)
    print(db)