from flask_app.models.schema_model import Schema
from flask_app.models.mtm_model import MtM

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

from flask_app.models.dog_model import Dog