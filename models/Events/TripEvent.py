from peewee import *
from models.BaseModel import BaseModel
from models.Customer import Customer
from models.Car import Car
from models.ChargingStation import ChargingStation
from models.WorkShop import Workshop


class TripEvent(BaseModel):
    event_id = IntegerField(primary_key=True)
    customer = ForeignKeyField(Customer)
    car = ForeignKeyField(Car)
    pickup_time = DateTimeField()
    end_time = DateTimeField()
    pickup_location = FloatField() # TODO: class location
    destination_location = FloatField()