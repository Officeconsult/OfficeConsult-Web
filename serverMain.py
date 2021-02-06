### - VV IMPORTS VV - ###
# import dependecies for flask
from flask import Flask, render_template, session, redirect, request
# database import
from flask_sqlalchemy import SQLAlchemy
# import for json - required for requests and stuff
import json, os, datetime, hashlib
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



### - VV CUSTOM DEFINE FUNCTIONS VV - ###
# used for constructing a clean database in a testing enviroment.
def constructDatabase():
    db.drop_all()
    db.create_all()

# my primary hash method, using 2 strings
def hashTwoStrings(string1, string2):
    m = hashlib.sha256()
    m.update(string1.encode('utf-8'))
    m.update(string2.encode('utf-8'))
    return m.digest()
### - ^^ CUSTOM DEFINE FUNCTIONS ^^ - ###



### - VV DATABASE MODELS VV - ###
# users and accounts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    emailConfirmed = db.Column(db.Boolean, nullable=False)
    confirmationEmailSent = db.Column(db.Boolean, nullable=False)
    hashedPassword = db.Column(db.String(100), nullable=False)
    hashSalt = db.Column(db.String(100), nullable=False)
    products = db.Column(db.PickleType)
    roles = db.Column(db.PickleType, nullable=False)
    dateJoined = db.Column(db.Date, nullable=False)
    # init when making new classes
    def __init__(self):
        self.products = []
        self.roles = ["new user"]
        self.dateJoined = datetime.date.today()
        self.hashSalt = str(os.urandom(30).hex())
        self.emailConfirmed = False
        self.confirmationEmailSent = False
    # representation when printed
    def __repr__(self):
        return f"USER: (username={self.username}, email={self.email})"
### - ^^ DATABASE MODELS ^^ - ###



### - VV ROUTES VV - ###
#V index returns homePage
@app.route("/")
def homepage_index():
    return render_template("homepage/HTML/index.html")

# login shows registration form, takes posts to make new user
@app.route("/login", methods=["GET"])
def homepage_login():
    login = session.get('login', False)
    if login:
        return redirect("/")
    # show registartion form if not logged in
    return render_template("homepage/HTML/login.html")

# post to make a new user
@app.route("/register-new-user", methods=['POST'])
def register_new_user():
    # try to make new user
    try:
        data = request.form
        newUser = User()
        newUser.username = data.get("Username")
        newUser.hashedPassword = hashTwoStrings(data.get('Password'), newUser.hashSalt)
        newUser.email = data.get("Email")
        db.session.add(newUser)
        db.session.commit()
    except Exception as e:
        print(e)
    return "TADA"

# if existing user is present
@app.route("/login-existing-user", methods=["POST"])
def login_existing_user():
    try:
        data = request.form
        u = User.query.filter_by(username=data.get("Username")).first()
        enteredPassword = hashTwoStrings(data.get('Password'), u.hashSalt)
        if enteredPassword == u.hashedPassword:
            session['username'] = u.username
        print(session)
    except Exception as e:
        print(e)
    return redirect("/login")
### - ^^ ROUTES ^^ - ###



### - VV EXECUTION VV - ###
# if main, run in debug mode
if __name__ == "__main__":
    app.debug = True
    app.run()
### - ^^ EXECUTION ^^ - ###
