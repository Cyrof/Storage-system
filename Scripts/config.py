from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from Scripts.secrets_folder import *
from urllib.parse import quote

conn = "mysql+pymysql://%s:%s@%s:%s/%s" % (dbuser, quote(
    dbpass), dbhost, dbport, dbname)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = conn

db = SQLAlchemy(app)

