from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/dojo")
def dojo():
    return "Dojo"

@app.route("/say/<name>")
def say(name):
    if not name.isdigit():
        return f"Hi, {name}"
    return "invalid request"

@app.route("/repeat/<times>/<word>")
def repeat(times,word):
    if times.isdigit() and not word.isdigit():
        return word * int(times)
    return "invalid request"

@app.route("/<var>")
def error(var):
    return "Sorry! No response. Try again."

if __name__=="__main__":
    app.run(debug=True)