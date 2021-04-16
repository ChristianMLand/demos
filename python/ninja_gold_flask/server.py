from flask import Flask, render_template, request, redirect, session
from random import randint
app = Flask(__name__)
app.secret_key ="itsasecret"

gold_map = {
    "farm" : (10,20),
    "cave" : (5,10),
    "house" : (2,5),
    "casino" : (-50,50),
    "test": (-300,300)
}

@app.route("/")
def index():
    if "gold" not in session:
        session["gold"] = 0
        session["activities"] = []
    return render_template("index.html",gold_map=gold_map)

@app.route("/<location>")
def process_money(location):
    if location in gold_map:
        amount = randint(*gold_map[location])
        color = "green" if amount > 0 else "red"
        session["activities"].append(f"<p style=color:{color}>Earned {amount} gold from the {location}!</p>")
        session["gold"] += amount
    return redirect("/")

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)