import os
import pathlib
import flask
from flask import Flask, session, render_template, request, redirect, url_for
import db
from db import User
from Group import Group
from werkzeug.utils import secure_filename
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
import requests
import enc
from google.auth.transport import requests as rq
from google.oauth2 import service_account

app = flask.Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar',"https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"]
#Database Code 

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['UPLOAD_FOLDER']= basedir+ "static/uploads"
app.config['MAX_CONTENT_PATH']= 150000
app.secret_key = os.environ.get("FLASK_SECRET_KEY", default="supersecretkey")

with open('keys/clientid.txt', 'rb') as p:
        c = p.read()
CLIENT_ID = enc.decrypt(c)

with open('keys/s.txt', 'rb') as p:
	s = p.read()
    
SECR= enc.decrypt(s)

client_secrets_file=os.path.join(pathlib.Path(__file__).parent,"client_secret.json")

session= {
"start": False,
"user": ""
}

@app.route("/")
def index():
  return render_template("index.html")
  
@app.route("/google-login")
def google_login():
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?"
                    f"response_type=code&client_id={CLIENT_ID}&"
                    f"redirect_uri={url_for('google_callback', _external=True)}&"
                    f"scope=openid%20email%20profile")

@app.route("/callback")
def google_callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    session["start"]= True

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": SECR,
        "redirect_uri": url_for('google_callback', _external=True),
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    try:
        token = r.json()["id_token"]
        claims = id_token.verify_oauth2_token(
            token,
            rq.Request(),
            CLIENT_ID
        )
        session["email"] = claims["email"]
        session["user"] = db.googleSignup(session.get("email"))
        print(session.get("user"))
        return flask.redirect('/home')
     
    except KeyError:
        return redirect(url_for("/home"))



@app.route('/signUp')
def signUp():
  return render_template("signUp.html")


@app.route('/signUp', methods=['POST'])
def trysignUp():
  signup = User().signUp()
  if (signup == True):
    session["user"] = signup
    return render_template("home.html")
  else:
    return render_template("signUp.html", alarm="1") 

@app.route('/login')
def login():
  if not session.get("user"):
    return render_template("login.html")
  return redirect('/home')

@app.route('/login', methods=["POST"])
def trylogin():
  data = request.form
  user = data.get("user")
  password = data.get("password")
  login = db.login(user, password)
  if (login != False):
    session['user'] = login
    return redirect('/home')
  else:
    return render_template("login.html", alarm="1")
    
@app.route('/home')
def home():
  if not session.get("user") and not session.get("email"):
    return redirect('/')
  if session.get("user").get("username"):
    return render_template("home.html", user=session.get("user").get("username"))
  if session.get("user").get("email"):
    return render_template("home.html", user= session.get("user").get("email"))

@app.route('/search')
def search():
        return render_template("search.html")
    
@app.route('/search1', methods=["GET"])
def searchDB():
    query= request.args.get('query')
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
        return render_template("results.html", len= len(results),
        results= results)
    else: 
        return render_template("results.html", len = 0, results= results)
    

@app.route('/settings')
def setting():
    return render_template("settings.html")
    
@app.route('/quiz')
def quiz():
    return render_template("quiz.html")
    
@app.route('/savequiz', methods= ["POST"])
def savequiz():
    data= request.form
    db.savequiz(data, 123)
    return render_template("quiz.html")

@app.route('/currentConvo')
def currentConvo():
    return render_template("currentConvo.html")

@app.route('/createGroup', methods = ["GET", "POST"])
def createGroup():
    if request.method == "POST":

        photo= request.files['groupPhoto']
        upload(photo)
        db.createChat(request, photo)
        return redirect('/existingGroups')
    return render_template("createGroup.html")
    
def upload(file):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

# #To avoid confusion
# @app.route('/existingGroups/V2')
# def userChats():
   
    # userchats= db.userChats(session.get("user").get("id"))

    # return render_template("existingGroups.html", len= len(userchats),results= userchats)

@app.route('/existingGroups')
def currentGroups():
    
    chats= []
    groupchats= db.existingChats("", "")
    return render_template("existingGroups.html", len= len(groupchats),results= groupchats)
#created a reloader for easier code running in localhost
#debug to find bugs
if __name__=='__main__':
    app.run(use_reloader= True, debug= True)
    
    
    
 