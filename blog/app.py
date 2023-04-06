from flask import Flask, request


app = Flask(__name__)



@app.route("/user/")
def index():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"