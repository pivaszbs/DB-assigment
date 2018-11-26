from peewee import *
from models.BaseModel import BaseModel
from models.Customer import Customer
from models.Car import Car
from models.WorkShop import Workshop
from models.Part import Part


class RepairingEvent(BaseModel):
    event_id = IntegerField(primary_key=True)
    customer = ForeignKeyField(Customer)
    workshop = ForeignKeyField(Workshop)
    part = ForeignKeyField(Part)
    car = ForeignKeyField(Car)
    price = IntegerField()
    time = DateTimeField()