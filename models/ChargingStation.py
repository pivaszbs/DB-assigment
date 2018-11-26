from peewee import *
from models.BaseModel import BaseModel


class ChargingStation(BaseModel):
    GPSx = FloatField()  # IDKrightnow
    GPSy = FloatField()
    CSUID = IntegerField(primary_key=True)
    time_of_charging = TimeField()
    available_sockets = IntegerField()