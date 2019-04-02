from flask import Flask, request, session, render_template, redirect, flash, url_for
import json
from functools import wraps

app = Flask(__name__.split('.')[0])
app.secret_key = 'Flask'

# we need to check to see if they're already logged in or not
# we just need a function

def logged_in():
    return 'user' in session

def collect_json():
    with open('json/users.json', 'r') as f:
        data = json.load(f)

    return data

def insert_json(json_data):
    with open('json/users.json', 'r+') as f:
        json.dump(json_data, f)

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
def hello_world():
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

    elif request.method == 'POST':
        print('collected data')
        print(request.form) 
        # this runs when someone hits "submit"
        # lol on the form in HTML, we forgot the button to send
        data = (request.form['username'], request.form['password'])
        if data[0] in collect_json():
            session['user'] = {'username': data[0]}
            return redirect("users")
        else:
            return render_template("login.html", error_code="1")


#########
# SIGNUP
#########       
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == 'GET':
        if not logged_in():
            return render_template("signup.html")

    elif request.method == 'POST':
        # this runs when someone hits "submit"
        # lol on the form in HTML, we forgot the button to send
        data = (request.form['username'], request.form['password'])
        if data[0] in collect_json():
            return render_template("signup.html", error_code="1")
        else:
            # make a new user!
            users_data = collect_json()
            users_data[data[0]] = data[1]
            insert_json(users_data)            
            return "It worked!"

#########
# USERS
#########
@app.route("/users", methods=['GET'])
def test():
    return render_template("users.html", users_list=collect_json())

@app.route("/users/<username>", methods=['GET'])
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
def error_404_page(error_code):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)