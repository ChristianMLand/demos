from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/dojo", methods=["POST"])
def dojo():
    print(request.form["name"])
    return redirect("/index")

@app.route("/index")
def html_test():
    print(request.method)
    return render_template("index.html")

@app.route("/say/<string:name>")
def say(name):
    return f"Hi, {name}"

@app.route("/repeat/<int:times>/<string:word>")
def repeat(times,word):
    return word * int(times)

if __name__=="__main__":
    app.run(debug=True)