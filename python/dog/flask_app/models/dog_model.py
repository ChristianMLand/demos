from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.schema_model import Schema

class Dog(Schema):
    def __init__(self, dog_id):
        super(dog_id)
    
    table = "dogs"
    db = "dogs_db"

    #any methods specific to dog go here