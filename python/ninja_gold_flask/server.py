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

settings = {
    "win" : 500,
    "moves" : 15
}

@app.route("/")
def index():
    if "gold" not in session:
        session["gold"] = 0
        session["activities"] = []
        session["moves"] = 0
        session["gameover"] = False
    return render_template("index.html",gold_map=gold_map)

@app.route("/<location>")
def process_money(location):
    if location in gold_map and not session["gameover"]:
        amount = randint(*gold_map[location])
        session["activities"].append(f"<p style=color:{'green' if amount > 0 else 'red'}>Earned {amount} gold from the {location}!</p>")
        session["gold"] += amount
        session["moves"] += 1
        won = session["gold"] >= settings["win"]
        if won or session["moves"] == settings["moves"]:
            session["gameover"] = True
            session["activities"].append(f"<p style=color:{'green>You won' if won else 'red>You lost'}!</p>")
    return redirect("/")

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)