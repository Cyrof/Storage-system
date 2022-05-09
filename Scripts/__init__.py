from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
import Scripts.secrets_folder as secrets_folder
from urllib.parse import quote

conn = "mysql+pymysql://%s:%s@%s:%s/%s" % (secrets_folder.dbuser, quote(
    secrets_folder.dbpass), secrets_folder.dbhost, secrets_folder.dbport, secrets_folder.dbname)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = conn

db = SQLAlchemy(app)

