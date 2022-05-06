from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# log in page
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('admin.html')

# sign up page 1
@app.route('/sign-up')
def sign_up():
    return render_template('sign-up1.html')

# sign up page 2
@app.route('/sign-up2')
def sign_up2():
    return render_template('sign-up2.html')

# home page
@app.route('/my-folder')
def home():
    return render_template('my-folder.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="8008")