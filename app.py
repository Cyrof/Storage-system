from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import secrets_folder
import pymysql

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
    secrets_folder.dbuser, secrets_folder.dbpass, secrets_folder.dbhost, secrets_folder.dbname)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = conn
db = SQLAlchemy(app)


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


@app.route('/sign-up')
def sign_up():
    return render_template('sign-up1.html')

# sign up page 2


@app.route('/sign-up2')
def sign_up2():
    return render_template('sign-up2.html')

# home page


@app.route('/my-folder')
def home():
    return render_template('my-folder.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="8008")
