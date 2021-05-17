from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.schema_model import Schema

class Dog(Schema):
    def __init__(self, dog_id):
        super(dog_id)
    
    table = "dogs"
    db = "dogs_db"

    @classmethod
    def add_toy(cls, **data):
        query = "INSERT INTO `dogs_has_dog_toys` (`dogs_id`, `dog_toys_id`) VALUES (%(dog_id)s,%(toy_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def remove_toy(cls, **data):
        query = "DELETE FROM `dogs_has_dog_toys` WHERE `dogs_id` = %(dog_id)s AND `dog_toys_id` = %(toy_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_toys(cls, **data):
        query = "SELECT dog_toys.* FROM `dogs_has_dog_toys` JOIN `dog_toys` ON `dog_toys_id`=dog_toys.id WHERE `dogs_id`=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)