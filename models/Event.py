from peewee import *
from models.BaseModel import BaseModel
from models.Customer import Customer
from models.WorkShop import Workshop


class Event(BaseModel):
    event_id = IntegerField(primary_key=True)
    type = CharField()
    customer = ForeignKeyField(Customer)
    workshop = ForeignKeyField(Workshop)
    start_time = DateTimeField()
    end_time = DateTimeField()
    pickup_location = FloatField() # TODO: create class location ?
    destination_location = FloatField()


    def generate_event(self, type, pickup_location, start_time, destination_location=None, end_time=None, customer=None, workshop=None):
        pass