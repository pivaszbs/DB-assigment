from peewee import *
from models.BaseModel import BaseModel

class Provider(BaseModel):
    name = CharField()
    phone_number = CharField()
    companyID = PrimaryKeyField()