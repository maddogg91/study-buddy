import os
import flask 
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

#Database Code 
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def index():
    return flask.render_template("index.html")

app.run()