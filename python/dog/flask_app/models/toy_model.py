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
    table = "dog_toys"
    
    def __init__(self, **data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")
        self._dogs_that_own = MtM(left=self,right=Dog,middle='dog_has_dog_toy')

    @property
    def dogs_that_own(self):
        return self._dogs_that_own.retrieve()
    
    @property
    def dogs_that_favorited(self):
        return Dog.retrieve(fav_toy_id=self.id)

@Toy.validator("Toy name is required!")
def name(val):
    return bool(val)

@Toy.validator("Toy name should be at least 3 characters!")
def name(val):
    return len(val) >= 3

@Toy.validator("Toy names should match!",match="name")
def confirm_name(val,match):
    return val == match

from flask_app.models.dog_model import Dog#at bottom because of circular import with Dog