import os


os.system("pip install pipreqs")

os.system("pipreqs ./ --encoding=utf-8 --ignore bin,etc,lib,lib64 --force")
os.system("pip install -r requirements.txt")
