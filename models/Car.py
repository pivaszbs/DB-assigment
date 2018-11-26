from peewee import *
from models.CarModel import CarModel


class Car(CarModel):
    location = CharField()
    car_id = IntegerField(primary_key=True)
