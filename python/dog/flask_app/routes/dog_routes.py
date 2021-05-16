from flask_app import app
from flask import render_template

from flask_app.models.dog_model import Dog

@app.route('/')
def index():
    return render_template('index.html', all_dogs=Dog.get_all())

@app.route('/dogs/<int:dog_id>')
def show_dog(dog_id):
    return render_template('view_dog.html', dog=Dog.get_one(id=dog_id))