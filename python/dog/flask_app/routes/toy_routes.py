from flask_app import app
from flask import render_template

from flask_app.models.toy_model import Toy

@app.route('/')
def index():
    return render_template('all_toys.html', all_toys=Toy.retrieve())

@app.route('/dogs/<int:toy_id>')
def show_toy(toy_id):
    return render_template('view_toy.html', toy=Toy.retrieve(id=toy_id))