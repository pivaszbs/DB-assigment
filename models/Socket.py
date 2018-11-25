from peewee import *
from models.BaseModel import BaseModel


class Socket(BaseModel):
    plug_type = CharField()
    plug_size = IntegerField()