from app import *
import string



class db_fun():

    def __init__(self):
        pass

    def get_id(self):
        alphabet = list(string.ascii_lowercase)
        userId_list = Users.query.order_by(Users.userId).all()
        print(userId_list[0])

if __name__ == "__main__":
    data = db_fun()
    data.get_id()
