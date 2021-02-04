from flask import Flask

app = Flask(__name__, template_folder="/content", static_folder="/content")

@app.route("/")
def index():
    return "hello world"

if __name__ == "__main__":
    app.run()