import flask
from flask import Flask, render_template, url_for, request, session, redirect, flash
import flask_pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask.ext.pymongo import PyMongo
import bcrypt

app = Flask(__name__)

#app.config['SECRET_KEY'] = 'testing'
app.config['MONGO_DBNAME'] = 'Basic_auth'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Basic_auth'
mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('Login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users2
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('SignUp.html')


"""@app.route('/')"""
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


if __name__ == "__main__":
    app.run(host = "localhost",port =5000,debug = True)