import os
import flask 
import db
from flask_bootstrap import Bootstrap
from db import User, groups
app = flask.Flask(__name__)

#Database Code 

basedir = os.path.abspath(os.path.dirname(__file__))
session_start= False

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route('/signUp')
def signUp():
    return flask.render_template("signUp.html")


@app.route('/signUp',methods=['POST'])
def trysignUp():
   signup= User().signUp()
   if(signup == True):
    session_start= True
    return flask.render_template("home.html")
   else:
    return flask.render_template("signUp.html", alarm= "1")   


@app.route('/login')
def login():
    return flask.render_template("login.html")

@app.route('/login', methods=["POST"])
def trylogin():
    data= flask.request.form
    user= data.get("user")
    password= data.get("password")
    login= db.login(user, password)
    if (login== True):
        session_start= True
        return flask.render_template("home.html")
    else:
        print("Invalid user")
        #We should add an alert for invalid login errors to HTML
        return flask.render_template("login.html", alarm= "1")
   
@app.route('/home')
def home():
    if(session_start== True):
        return flask.render_template("home.html")
    else:
        return flask.render_template("index.html")

@app.route('/search')
def search():
    return flask.render_template("search.html")

@app.route('/settings')
def setting():
    return flask.render_template("settings.html")

@app.route('/currentConvo')
def currentConvo():
    return flask.render_template("currentConvo.html")

@app.route('/createGroup')
def createGroup():
    return flask.render_template("createGroup.html")

@app.route('/existingGroups')
def existingGroups():
    groups.first=groups
    return flask.render_template("existingGroups.html",groups=groups)

#created a reloader for easier code running in localhost
#debug to find bugs
if __name__=='__main__':
    app.run(use_reloader= True, debug= True)