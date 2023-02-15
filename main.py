import os
import pathlib
from symbol import flow_stmt
import flask 
import db
from db import User
import time
from Group import Group
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

app = flask.Flask(__name__)
GOOGLE_CLIENT_ID="722336652195-mej9vpifk9raoivrvo579imk2v58jjhu.apps.googleusercontent.com"
client_secrets_file=os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow=Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
    )

#Database Code 

basedir = os.path.abspath(os.path.dirname(__file__))

session= {
"start": False,
"user": ""
}


@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route('/signUp')
def signUp():
    return flask.render_template("signUp.html")

@app.route('/signUp')
def googleSignup():
    authorization_url,state=flow.authorization_url()
    session["state"]=state
    return flask.redirect(authorization_url) 
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
def findGroupSearch():
    keyword= flask.request.args.get('q')
    chats= []
    groupchats= db.searchForGroupChat(keyword, "name")
    return flask.render_template("results.html", len= len(groupchats),
    results= groupchats)
    

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
def currentGroups():
    chats= []
    groupchats= db.existingChats()
    return flask.render_template("existingGroups.html", len= len(groupchats),results= groupchats)
#created a reloader for easier code running in localhost
#debug to find bugs
if __name__=='__main__':
    app.run(use_reloader= True, debug= True)