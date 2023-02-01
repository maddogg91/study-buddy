import os
import flask 
import db


app = flask.Flask(__name__)

#Database Code 
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route('/signUp')
def signUp():
    return flask.render_template("signUp.html")

@app.route('/login')
def login():
    return flask.render_template("login.html")

@app.route('/-login')
def trylogin():
    #TODO: Add a POST form to login HTML to return user and password
    #Test values user and passw can be changed to test implementation until POST is added
    user= "test"
    password= "test"
    login= db.login(user, password)
    if (login== True):
        return flask.render_template("home.html")
    else:
        print("Invalid user")
        #We should add an alert for invalid login errors to HTML
        return flask.render_template("login.html")
   
@app.route('/home')
def home():
    return flask.render_template("home.html")

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
    return flask.render_template("existingGroups.html")

#created a reloader for easier code running in localhost
#debug to find bugs
if __name__=='__main__':
    app.run(use_reloader= True, debug= True)