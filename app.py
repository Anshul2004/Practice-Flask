from flask import Flask, request, session, render_template, redirect, flash, url_for
import json
from functools import wraps
import pyrebase

app = Flask(__name__.split('.')[0])
app.secret_key = 'sf651456se561sef156se156sef1653sfe1653sf1sf1f1s32sffsf35f1313s3ss1fs1f51651416s551'


config = {
    "apiKey": "AIzaSyAyPZb_cuRLwt5-lhJECzNTRz8QAGhI-PM",
    "authDomain": "flask-test-31ade.firebaseapp.com",
    "databaseURL": "https://flask-test-31ade.firebaseio.com",
    "projectId": "flask-test-31ade",
    "storageBucket": "flask-test-31ade.appspot.com",
    "messagingSenderId": "522452899767"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.child("names").push({"name": "Anshul the god"})

# Firebase Functions

def input_data(data, database):
    db.child(database).push(data)

def remove_data(data, database):
    db.child(database).remove(data)

def view_data(database):
    # kk since this is all based off python
    #db.child(database).

# this is firebase?
#^


def logged_in():
    '''returns bool
    if the user is logged in'''
    return 'user' in session

def collect_json(database='users'):
    '''gets data into json file
    database defaults to 'users'
    '''
    with open('json/' + database + '.json', 'r') as f:
        data = json.load(f)

    return data

def insert_json(json_data, database='users'):
    '''reputs data into json file
    database defaults to 'users'
    '''
    with open('json/' + database + '.json', 'r+') as f:
        json.dump(json_data, f)
        
# Login Wrap
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if logged_in():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_page'))
    return wrap
            

#######
# HOME
#######
@app.route('/')
def home_page():
    return render_template('index.html')


########
# LOGIN
########
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        if not logged_in():
            print('Session is >' + str(session))
            return render_template("login.html")

        # Logged In already
        return redirect(url_for('users_page', username=session['user']['username']))

    # Form input
    elif request.method == 'POST':
        data = (request.form['username'], request.form['password'])
        users_database = collect_json()
        
        # Logged in!
        if data[0] in users_database and data[1] == users_database[data[0]]["password"]:
            session['user'] = {'username': data[0]}
            return redirect(url_for('users_page', username=session['user']['username']))
        # Invalid login information
        else:
            return render_template("login.html", error_code="1")

######

"""
"""


#########
# LOGOUT
#########
@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    if request.method == 'GET':
        return render_template('logout.html')
        
    elif request.method == 'POST':
        del session['user']
        return redirect(url_for("home_page"))

#########
# SIGNUP
#########       
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == 'GET':
        if not logged_in():
            return render_template("signup.html")

    # Form input
    elif request.method == 'POST':
        data = (request.form['username'], request.form['password'], request.form['email'])
        users_database = collect_json()

        if data[0] in users_database or data[2] in [users_database[i]['email'] for i in users_database]:
            return render_template("signup.html", error_code="1")
        else:
            # make a new user!
            users_data = collect_json()
            users_data[data[0]] = {"password": data[1], "email": data[2]}
            insert_json(users_data)            
            return "It worked!"

#########
# USERS
#########
@app.route("/users", methods=['GET'])
# i.e. /users
def test():
    return render_template("users.html", users_list=collect_json())


@app.route("/users/<username>", methods=['GET'])
# i.e. /users/admin
@login_required
def users_page(username):
    print('1')

    # Show all users
    if username is None:
        return render_template("users.html", users_list=collect_json())
    
    # Show username page
    else:
        if username in collect_json():
            return "Hello " + username
        else:
            return render_template('404.html')


@app.errorhandler(404)
# i.e. if a website doesn't exist (404 error code)
def error_404_page(error_code):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)