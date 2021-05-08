from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    print(request.method)
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def orocess():
    print(request.method)
    print(request.form)
    return redirect(f"/repeat/{request.form['times']}/{request.form['name']}")

@app.route("/repeat/<int:times>/<string:word>")
def repeat(times,word):
    print(request.method)
    return word * times

if __name__=="__main__":
    app.run(debug=True)