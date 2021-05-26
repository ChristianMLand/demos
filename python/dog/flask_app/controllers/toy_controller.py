from flask import redirect, request, render_template
from flask_app import app
from flask_app.models.toy_model import Toy

#---------------Render Routes-------------------#
@app.route('/toys')
def all_toys():
    return render_template('all_toys.html', all_toys=Toy.retrieve())

@app.route('/toys/<int:toy_id>')
def show_toy(toy_id):
    return render_template('view_toy.html', toy=Toy.retrieve(id=toy_id)[0])
#---------------Action Routes-------------------#
@app.route('/toys/create', methods=['POST'])
def create_toy():
    if Toy.validate(**request.form):
        Toy.create(**request.form)
    return redirect('/toys')
#-----------------------------------------------#