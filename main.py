import os
from symbol import flow_stmt
import flask
from flask import Flask, redirect, url_for, session
import db
from db import User
from Group import Group
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.transport import requests
import google.auth.transport.requests
app = flask.Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/calendar',"https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"]
#Database Code 

basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = os.environ.get("FLASK_SECRET_KEY", default="supersecretkey")

CLIENT_ID = "722336652195-mej9vpifk9raoivrvo579imk2v58jjhu.apps.googleusercontent.com"

session= {
"start": False,
"user": ""
}
@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/google-login")
def google_login():
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?"
                    f"response_type=code&client_id={CLIENT_ID}&"
                    f"redirect_uri={url_for('google_callback', _external=True)}&"
                    f"scope=openid%20email%20profile")

@app.route("/callback")
def google_callback():
    code = requests.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": "your_client_secret_here",
        "redirect_uri": url_for('google_callback', _external=True),
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    id_token = r.json()["id_token"]
    claims = id_token.verify_oauth2_token(
        requests.Request(),
        CLIENT_ID
    )
    session["email"] = claims["email"]
    return redirect(url_for("home"))
@app.route('/signUp')
def signUp():
    return flask.render_template("signUp.html")


@app.route('/signUp',methods=['POST'])
def trysignUp():
   signup= User().signUp()
   if(signup == True):
    session["start"]= True
    return flask.render_template("home.html")
   else:
    return flask.render_template("signUp.html", alarm= "1")   

@app.route('/login')
def login():
    if(session["start"]== True):
        return flask.redirect('/home')
    return flask.render_template("login.html")

@app.route('/login', methods=["POST"])
def trylogin():
    if(session["start"]== True):
        return flask.redirect('/home')

    data= flask.request.form
    user= data.get("user")
    password= data.get("password")
    login= db.login(user, password)
    if (login!= False):
        session["start"]= True
        #adds user login information to session object
        session["user"]= login
        return flask.redirect('/home')
    else:
        #Alarm set to 1 triggers alert on front end.
        return flask.render_template("login.html", alarm= "1")
    
   
@app.route('/home')
def home():
    if(session["start"]== True):
        #sends user information to home.html
        return flask.render_template("home.html", user= session["user"]["username"])
    else:
        return flask.redirect('/')

@app.route('/search')
def search():
        return flask.render_template("search.html")
    
@app.route('/search1', methods=["GET"])
def searchDB():
    query= flask.request.args.get('query')
    query= query.split(": ")
    if(len(query) < 2):
        results = db.existingChats(query[0], "name")
    else:  
        flter= query[0].strip()
        keyword= query[1]
        chats= []
        #searches DB by username
        if(flter== "user"):
            results= db.searchUsers(keyword, "username")
        #searches DB by group name    
        elif(flter== "group"):
            results= db.existingChats(keyword, "name")
        #searches DB by group description    
        elif(flter== "gdesc"):
            results= db.existingChats(keyword, "description")
        #search DB by user messages coming soon    
    if results != "No results found...":
        return flask.render_template("results.html", len= len(results),
        results= results)
    else: 
        return flask.render_template("results.html", len = 0, results= results)
    

@app.route('/settings')
def setting():
    return flask.render_template("settings.html")
    
@app.route('/quiz')
def quiz():
    return flask.render_template("quiz.html")
    
@app.route('/savequiz', methods= ["POST"])
def savequiz():
    data= flask.request.form
    db.savequiz(data, 123)
    return flask.render_template("quiz.html")

@app.route('/currentConvo')
def currentConvo():
    return flask.render_template("currentConvo.html")

@app.route('/createGroup', methods = ["GET", "POST"])
def createGroup():
    if flask.request.method == "POST":
        db.createChat(flask.request.form)
    return flask.render_template("createGroup.html")

@app.route('/existingGroups')
def currentGroups():
    chats= []
    groupchats= db.existingChats("", "")
    return flask.render_template("existingGroups.html", len= len(groupchats),results= groupchats)
#created a reloader for easier code running in localhost
#debug to find bugs
if __name__=='__main__':
    app.run(use_reloader= True, debug= True)