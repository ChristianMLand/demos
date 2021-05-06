from flask import Flask
import random
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/dojo")
def dojo():
    return "Dojo"

@app.route("/repeat/<times>/<word>")
def repeat(times='1',word="test"):
    if times.isdigit() and not word.isdigit():
        return word * int(times)
    return "invalid request"

@app.route("/say/<word>")
def say(word):
    if not word.isdigit():
        return "Hi, " + word
    return "invalid request"

@app.route("/<var>")
def error(var):
    return "Sorry! No response. Try again."

if __name__=="__main__":
    app.run(debug=True)