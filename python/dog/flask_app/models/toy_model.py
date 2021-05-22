from flask_app.models.schema_model import Schema
from flask_app.models.mtm_model import MtM

'''
Toy.create(name="Ball") -> should create new toy in db
all_toys = Toy.retrieve() -> should return all toys
toy = Toy.retrieve(id=1) -> should return the toy with id=1
toy.dogs_that_own.retrieve() -> should return a list of all the dogs that own the toy with id=1
toy.dogs_that_favorited -> should return a list of all the dogs that favorited the toy with id=1
'''
class Toy(Schema):
    def __init__(self, **data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")
        self._dogs_that_own = MtM(left_table=self,right_table=Dog,middle_table='dog_has_dog_toy')

    @property
    def dogs_that_own(self):
        return self._dogs_that_own.retrieve()
    
    @property
    def dogs_that_favorited(self):
        return Dog.retrieve(fav_toy_id=self.id)

    table = "dog_toys"

from flask_app.models.dog_model import Dog#circular import with Dog