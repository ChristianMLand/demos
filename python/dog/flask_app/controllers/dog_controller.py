from flask import redirect, request, render_template
from flask_app import app
from flask_app.models.toy_model import Toy
from flask_app.models.dog_model import Dog


#---------------Display Routes-------------------#
@app.route('/')
def index():
    context = {
        "all_dogs" : Dog.retrieve(),
        "all_toys" : Toy.retrieve()
    }
    return render_template('index.html', **context)

@app.route('/dogs/<int:dog_id>')
def show_dog(dog_id):
    this_dog = Dog.retrieve(id=dog_id)[0]
    context = {
        "dog" : this_dog,
        "all_toys": Toy.retrieve(),
        "owned_toys": this_dog.owned_dog_toys.retrieve()
    }
    return render_template('view_dog.html', **context)
#---------------Action Routes-------------------#
@app.route('/dogs/create', methods=['POST'])
def create_dog():
    if Dog.validate(**request.form):
        Dog.create(**request.form)
    return redirect('/')

@app.route('/dogs/<int:dog_id>/add-toy', methods=['POST'])
def give_toy(dog_id):
    this_dog = Dog.retrieve(id=dog_id)[0]
    this_toy = Toy.retrieve(id=request.form['toy_id'])[0]
    this_dog.owned_dog_toys.add(this_toy)
    return redirect(f'/dogs/{dog_id}')

@app.route('/dogs/<int:dog_id>/remove-toy/<int:toy_id>')
def take_toy(dog_id,toy_id):
    this_dog = Dog.retrieve(id=dog_id)[0]
    this_toy = Toy.retrieve(id=toy_id)[0]
    this_dog.owned_dog_toys.remove(this_toy)
    return redirect(f'/dogs/{dog_id}')
#-----------------------------------------------#