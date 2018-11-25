from peewee import *
from models.BaseModel import BaseModel


class Workshop(BaseModel):
    WID = IntegerField(primary_key=True)
    availability_of_timing = TimeField()
