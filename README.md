#—-Instructions—-
Download file either clone to repo or download via zip file. 
Once downloaded create venv then run run.py from folder

#Create venv 
```console
root@localhost:~$ pip install virtualenv
root@localhost:~$ cd "folder-downloaded"
root@localhost:~$ python -m venv venv_name
```
After creating venv, you need to activate it then run the run.py to install all libraries and packages

#Activate venv and running run.py
```console
root@localhost:~$ venv_name\Scripts\activate
(venv_name)root@localhost:~$py run.py
```
After running run.py and installing all libraries and packages, you can now run app.py to start the flask server by writing this set of command in the terminal
```console
(venv_name)root@localhost:~$py app.py
```
