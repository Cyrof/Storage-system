import mysql.connector
import secrets_folder

new_db = mysql.connector.connect(
    host=secrets_folder.dbhost, # usually host='localhost' if you user root to create db
    user=secrets_folder.dbuser,
    passwd=secrets_folder.dbpass,
    database=secrets_folder.dbname
)

mycursor = new_db.cursor()

mycursor.execute("show")

# mycursor.execute('create database StorageSystem')