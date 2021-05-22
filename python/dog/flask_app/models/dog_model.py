from flask_app.models.schema_model import Schema
from flask_app.models.mtm_model import MtM

'''
dog = Dog.retrieve(id=1) -> should give dog with id=1
dog.toys.retrieve() -> should give all toys associated with the dog id=1
dog.toys.retrieve(id=1) -> should give toy that has the id=1 and is associated with dog id=1
all_toys = Toy.retrieve() -> should give all toys
first_toy = Toy.retrieve(id=1) -> should give toy with id=1
'''
class Dog(Schema):
    def __init__(self, **data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.type = data.get('type')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self._fav_toy_id = data.get('fav_toy_id')
        self._owned_dog_toys = MtM(left_table=self,right_table=Toy,middle_table='dog_has_dog_toy')
    table = "dogs"

    @property
    def owned_dog_toys(self):
        return self._owned_dog_toys

    @property
    def fav_toy(self):
        return Toy.retrieve(id=self._fav_toy_id)[0];

from flask_app.models.toy_model import Toy