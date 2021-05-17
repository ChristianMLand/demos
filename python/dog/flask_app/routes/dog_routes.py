from flask_app import app
from flask import render_template

from flask_app.models.dog_model import Dog
from flask_app.models.toy_model import Toy

@app.route('/')
def index():
    return render_template('index.html', all_dogs=Dog.retrieve())

@app.route('/dogs/<int:dog_id>')
def show_dog(dog_id):
    context = {
        "dog" : Dog.retrieve(id=dog_id)[0],
        "all_toys": Toy.retrieve(),
        "owned_toys" : Dog.get_toys(id=dog_id)
    }
    return render_template('view_dog.html', **context)