from flask_app import app
from flask import redirect, request

from flask_app.models.toy_model import Toy

@app.route('/toys/create', methods=['POST'])
def create_toy():
    Toy.create(
        name=request.form['name']
    )
    return redirect('/')