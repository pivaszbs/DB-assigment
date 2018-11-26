from peewee import *
from models.BaseModel import BaseModel
from models.Car import Car
from models.Socket import Socket


class Charging(BaseModel):
    CarID = ForeignKeyField(Car, backref='charging_car')
    # It's just relation
    plug_type = ForeignKeyField(Socket, field='plug_type')
    plug_size = ForeignKeyField(Socket, field='plug_size')
