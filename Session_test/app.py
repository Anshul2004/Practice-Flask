'''
from flask import Flask, request, session, render_template, redirect, flash, url_for
import json
from functools import wraps

app = Flask(__name__.split('.')[0])
app.secret_key = 'sf651456se561sef156se156sef1653sfe1653sf1sf1f1s32sffsf35f1313s3ss1fs1f51651416s551'

@app.route("username/<username>")
def session_test(username):
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' +  "<b><a href = '/logout'>click here to log out</a></b>"
        #could add something like online... it has a link to "click here to log in"
        
    return "You are not logged in <br><a href= '/login'></b>" + "click here to log in</b></a>"
    '''    
'''

'''