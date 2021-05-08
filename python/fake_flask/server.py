from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/dojo")
def dojo():
    return "Dojo"

@app.route("/index")
def html_test():
    return render_template("index.html")

@app.route("/say/<string:name>")
def say(name):
    return f"Hi, {name}"

@app.route("/repeat/<int:times>/<string:word>")
def repeat(times,word):
    return word * int(times)

if __name__=="__main__":
    app.run(debug=True)