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


### - VV DEVELOPMENT DEF VV - ###
# used for constructing a clean database in a testing enviroment.
def constructDatabase():
    db.drop_all()
    db.create_all()
### - ^^ DEVELOPMENT DEF ^^ - ###


### - VV DATABASE MODELS VV - ###
# users and accounts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    emailConfirmed = db.Column(db.Boolean, nullable=False)
    hashedPassword = db.Column(db.String(100), nullable=False)
    hashSalt = db.Column(db.String(100), nullable=False)
    products = db.Column(db.PickleType)
    roles = db.Column(db.PickleType, nullable=False)
    # representation when printed
    def __repr__(self):
        return f"USER: (username={self.username}, email={self.email})"
### - ^^ DATABASE MODELS ^^ - ###


### - VV ROUTES VV - ###
# index returns homePage
@app.route("/")
def index():
    method_was_get = request.method == "GET"
    if method_was_get:
        print("GOT IT")
    return render_template("homepage/HTML/index.html")
# if already logged in redir, else show registration form
@app.route("/register", methods=["GET","POST"])
def dealmakerIndex():
    # if Get::
    if request.method == "GET":
        print("method was get")
        login = session.get('login', False)
        if login:
            print("already logged in")
            return redirect("/")
        # show registartion form if not logged in
        print("NOT logged in")
        return render_template("homepage/HTML/register.html")
    # if the method is post::
    if request.method == "POST":
        data = request.form
        print(data)
    return "TADA"
### - ^^ ROUTES ^^ - ###


### - VV EXECUTION VV - ###
# if main, run in debug mode
if __name__ == "__main__":
    app.debug = True
    app.run()
### - ^^ EXECUTION ^^ - ###
