from peewee import *
from models.BaseModel import BaseModel


class ResidentialAddress(BaseModel):
    country = CharField()
    city = CharField()
    zip = IntegerField(primary_key=True)
