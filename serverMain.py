from flask import Flask, render_template, session
import json

config = {}

with open("config.json", "r") as file:
    config = json.loads(file.read())

app = Flask(__name__, template_folder="/content", static_folder="/content")
app.secret_key = config.get("secretCookieKey")


@app.route("/")
def index():
    print(session)
    return "hello world"

if __name__ == "__main__":
    app.run()