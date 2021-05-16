from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.schema_model import Schema

class Toy(Schema):
    def __init__(self, toy_id):
        super(toy_id)
    
    table = "dog_toys"
    db = "dogs_db"