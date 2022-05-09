import mysql.connector
import Scripts.secrets_folder as secrets_folder

new_db = mysql.connector.connect(
    host=secrets_folder.dbhost, # usually host='localhost' if you user root to create db
    user=secrets_folder.dbuser,
    passwd=secrets_folder.dbpass,
)

mycursor = new_db.cursor()

mycursor.execute('create database StorageSystem')