from flask import Flask, request, session, render_template, redirect, flash, url_for
import json

app = Flask(__name__)
app.secret_key = 'RIDHISHUL4LIFE <-- I agree (Apollo)'

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
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == 'POST':
        pass
        # do some verfication
        #session['user'] = {'username': username}


#########
# SIGNUP
#########       
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == 'GET':
        if not logged_in():
            print('Session is >' + str(session))
            return render_template("signup.html")

    elif request.method == 'POST':
        print('collected data')
        print(request.form) 
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

if __name__ == '__main__':
    app.run(debug=True)