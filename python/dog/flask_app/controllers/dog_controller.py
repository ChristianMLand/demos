from flask_app import app
from flask import redirect, request, render_template

from flask_app.models.dog_model import Dog
from flask_app.models.toy_model import Toy

#---------------Render Routes-------------------#
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
#---------------Action Routes-------------------#
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
#-----------------------------------------------#