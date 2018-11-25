from peewee import *
from models.BaseModel import BaseModel
from models.Customer import Customer
from models.Car import Car
from models.ChargingStation import ChargingStation
from models.WorkShop import Workshop


class ChargingEvent(BaseModel):
    event_id = IntegerField(primary_key=True)
    customer = ForeignKeyField(Customer)
    charging_station = ForeignKeyField(ChargingStation)
    car = ForeignKeyField(Car)
    time = DateTimeField()