from peewee import *
from models.BaseModel import BaseModel
from models.Customer import Customer
from models.Car import Car


class TripEvent(BaseModel):
    event_id = IntegerField(primary_key=True)
    customer = ForeignKeyField(Customer)
    car = ForeignKeyField(Car)
    pickup_time = DateTimeField()
    end_time = DateTimeField()
    pickup_location = CharField()
    destination_location = CharField()
    distance_to_user = IntegerField()
    trip_duration = IntegerField()
