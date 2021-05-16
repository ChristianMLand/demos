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