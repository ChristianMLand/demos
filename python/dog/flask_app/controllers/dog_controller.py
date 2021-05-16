from flask_app import app
from flask import redirect, request

from flask_app.models.dog_model import Dog

@app.route('/dogs/create', methods=['POST'])
def create_dog():
    Dog.create(
        name=request.form['name'],
        type=request.form['type']
    )
    return redirect('/')

@app.route('/dogs/<int:dog_id>/add-toy', methods=['POST'])
def give_toy(dog_id):
    Dog.add_toy(
        dog_id=dog_id,
        toy_id=request.form['toy_id']
    )
    return redirect(f'/dogs/{dog_id}')

@app.route('/dogs/<int:dog_id>/remove-toy/<int:toy_id>')
def take_toy(dog_id,toy_id):
    Dog.remove_toy(
        dog_id=dog_id,
        toy_id=toy_id
    )
    return redirect(f'/dogs/{dog_id}')