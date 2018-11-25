from peewee import *
from models.BaseModel import BaseModel
from models.ResidentalAddress import ResidentialAddress


class Customer(BaseModel):
    phone = CharField()
    email = CharField(unique=True)
    residential_address = ForeignKeyField(ResidentialAddress, field='zip')
    username = CharField(primary_key=True)
    full_name = CharField()