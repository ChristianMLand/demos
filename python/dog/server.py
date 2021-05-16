from flask_app import app

from flask_app.controllers import  dog_controller, toy_controller
from flask_app.routes import dog_routes

if __name__=="__main__":
    app.run(debug=True)