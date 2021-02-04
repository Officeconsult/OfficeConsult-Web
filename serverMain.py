# import dependecies
from flask import Flask, render_template, session, redirect, request
import json

# set the config from the config.json -> file is ignored by git
config = {}
with open("config.json", "r") as file:
    config = json.loads(file.read())

# make the WSGI-App object, set the keys and refferences
app = Flask(__name__, template_folder="/content", static_folder="/content")
app.secret_key = config.get("secretCookieKey")


### VV ROUTES VV ###
# index returns homePage
@app.route("/")
def index():
    return "hello world"

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
### ^^ ROUTES ^^ ###


# if main, run in debug mode
if __name__ == "__main__":
    app.debug = True
    app.run()