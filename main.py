import os
import flask 
import db
from db import User
import time
from Group import Group
app = flask.Flask(__name__)

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
        results= db.existingChats(query,"")
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