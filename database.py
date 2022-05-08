import string
import mysql.connector
import secrets_folder
import re

db = mysql.connector.connect(
    host="127.0.0.1",
    user="Cyrof",
    passwd="B@sketba1lF@te0331",
    database="storagesystem"
)

mycursor = db.cursor(buffered=True)

class db_fun():

    def __init__(self):
        self.mycursor = db.cursor()
        pass

    def create_id(self):
        alphabets = list(string.ascii_lowercase)
        query = 'select userId from users'
        mycursor.execute(query)
        Id_list = [re.split('(\d+)', str(x[0])) for x in mycursor]
        alphabet_index = [0]
        counter = 1
        max_num = 99
        current_num = int(Id_list[-1][1])
        missing_num = self.check_id(Id_list)

        while True:
            if current_num <= max_num:
                userid = alphabets[alphabet_index[-1]] + str(missing_num)
                break
            elif current_num > max_num:
                max_num += 99
                counter += 1
                alphabet_index.append(counter)
                continue

        print(userid)
    
    def check_id(self, id_list):
        total_sum = 0
        for x in range(len(id_list)):
            total_sum += int(id_list[x][1])
        n = len(id_list) + 1
        total_list_of_sum = n * (n + 1) // 2
        return total_list_of_sum - total_sum


if __name__ == "__main__":
    data = db_fun()
    data.create_id()
