from peewee import *
from models.BaseModel import BaseModel
from models.ResidentalAddress import ResidentialAddress


class Customer(BaseModel):
    c_id = PrimaryKeyField()
    phone_number = CharField()
    email = CharField(unique=True)
    residential_address = ForeignKeyField(ResidentialAddress, field='zip')
    username = CharField()
    full_name = CharField()
