from email.policy import default
import string
from psutil import users
import re
from Scripts.config import db

# Users table


class Users(db.Model):
    userId = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(50))
    passwd = db.Column(db.String(100))
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(225))
    authority = db.Column(db.String(20), default='user')

# authenticate table


class Authenticate(db.Model):
    uid = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(225))
    key = db.Column(db.String(32))
    confirmation_status = db.Column(db.String(50), default='waiting')


# class that contains all db functions / arithmetic
class db_fun():

    def __init__(self):
        pass

    # create id function
    def create_uid(self):
        # call User class to get all user info into list as user class. Than get userId and split it
        users = Users.query.all()
        Id_list = [re.split('(\d+)', str(users[x].userId))
                   for x in range(len(users))]

        alphabets = list(string.ascii_lowercase)
        # check id list if there is user
        if Id_list == []:
            current_num = 0
        else:
            current_num = int(Id_list[-1][1])
        alphabet_index = [0]
        counter = 1
        max_num = 99
        # get missing num or higherst num for num id
        missing_num = self.check_id(Id_list)

        # while loop to check for index for alphabet and creation of userid
        while True:
            if current_num <= max_num:
                userid = alphabets[alphabet_index[-1]] + str(missing_num)
                return userid
            elif current_num > max_num:
                max_num += 99
                counter += 1
                alphabet_index.append(counter)
                continue

    # function to check for missing number/id from userid in db
    def check_id(self, id_list):
        total_sum = 0
        for x in range(len(id_list)):
            total_sum += int(id_list[x][1])
        n = len(id_list) + 1
        total_list_of_sum = n * (n + 1) // 2
        return total_list_of_sum - total_sum

    def create_eid(self):
        id = Authenticate.query.all()
        Id_list = [id[x].uid for x in range(len(id))]

        if Id_list == []:
            newId = 1
        else:
            newId = int(Id_list[-1]) + 1
        return newId


if __name__ == "__main__":
    data = db_fun()
    id = data.create_id()
    print(id)
