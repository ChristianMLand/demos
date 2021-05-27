from flask_app.models.schema_model import Schema
from flask_app.models.mtm_model import MtM

class Dog(Schema):
    table = "dogs"

    def __init__(self, **data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.type = data.get('type')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self._fav_toy_id = data.get('fav_toy_id')
        self._owned_dog_toys = MtM(left=self,right=Toy,middle='dog_has_dog_toy')

    @property
    def owned_dog_toys(self):
        return self._owned_dog_toys

    @property
    def fav_toy(self):
        return Toy.retrieve(id=self._fav_toy_id)[0];

@Dog.validator("Dog name is required!")
def name(val):
    return bool(val)

@Dog.validator("Dog name should be at least 3 characters long!")
def name(val):
    return len(val) >= 3

@Dog.validator("Dog type is required!")
def type(val):
    return bool(val)

@Dog.validator("Dog type should be at least 3 characters long!")
def type(val):
    return len(val) >= 3

from flask_app.models.toy_model import Toy#at bottom because of circular import with Toy