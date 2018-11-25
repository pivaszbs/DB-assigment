from peewee import *
from models.BaseModel import BaseModel


class Workshop(BaseModel):
    availabilty_of_timing = TimeField()
    WID = IntegerField(primary_key=True)