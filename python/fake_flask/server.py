from flask import Flask

app = Flask(__name__)

users = [
    {"name":"chris"},
    {"name":"tyler"},
    {"name":"jim"}
]

@app.route("/")
def root():
    print("Hello World")
    return "this is my root"

@app.route("/users/<id>")
def display_user(id):
    if id.isdigit() and int(id) in range(len(users)):
        return users[int(id)]
    else:
        return "invalid user id"

@app.route("/<word>")
@app.route("/<word>/<times>")
def mult_decos_test(word,times='1'):
    if times.isdigit():
        return word * int(times)
    return "invalid number of times"

if __name__=="__main__":
    app.run(debug=True)