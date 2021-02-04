### - VV IMPORTS VV - ###
# import dependecies for flask
from flask import Flask, render_template, session, redirect, request
# database import
from flask_sqlalchemy import SQLAlchemy
# import for json - required for requests and stuff
import json
### - ^^ IMPORTS ^^ - ###


### - VV APPLICATION SETUP / CONFIGURATION VV - ###
# this sets the config from the config.json (file is ignored by git - must be made locally)
config = {}
with open("config.json", "r") as file:
    config = json.loads(file.read())
# make the WSGI-App object, configure secrets
app = Flask(__name__, template_folder="content", static_folder="content")
app.secret_key = config.get("secretCookieKey")
# config the database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///testbase.db"
db = SQLAlchemy(app)
### - ^^ APPLICATION SETUP / CONFIGURATION ^^ - ###


### - VV DATABASE MODELS VV - ###
# users and accounts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashedPassword = db.Column(db.String(100), nullable=False)
    hashSalt = db.Column(db.String(100), nullable=False)
    products = db.Column(db.PickleType)
    # representation when printed
    def __repr__(self):
        return f"USER: (username={self.username}, email={self.email})"
    # constructor for new users
    def __init__(self, username, email, hashedPassword, hashSalt):
        self.username = username
        self.email = email
        self.hashedPassword = hashedPassword
        self.hashSalt = hashSalt
### - ^^ DATABASE MODELS ^^ - ###


### - VV ROUTES VV - ###
# index returns homePage
@app.route("/")
def index():
    return render_template("homepage/HTML/index.html")
# if logged in, render dealmaker, else redir -> index
@app.route("/dealmaker")
def dealmakerIndex():
    login = session.get('login', False)    
    access = "dealMaker" in session.get('products', [])
    if login and access:
        print("logged in")
    else:
        print("NOT logged in")
    return redirect("/")
### - ^^ ROUTES ^^ - ###


### - VV EXECUTION VV - ###
# if main, run in debug mode
if __name__ == "__main__":
    app.debug = True
    app.run()
### - ^^ EXECUTION ^^ - ###
