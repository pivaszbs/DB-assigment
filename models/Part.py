from peewee import *
from models.BaseModel import BaseModel

class Part(BaseModel):
    name = CharField()