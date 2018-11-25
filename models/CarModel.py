from peewee import *
from models.BaseModel import BaseModel

class CarModel(BaseModel):
    CMID = IntegerField(primary_key=True)
    name = CharField()
    power = IntegerField()
    color = CharField()
