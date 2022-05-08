import os


os.system('pip install -r requirements.txt')

secret_key = os.urandom(12).hex()

with open('secrets_folder.py', 'a+') as f:
    f.write('\n' + f'''\
        secret_key = '{secret_key}'
        ''')
print('Execution completed')