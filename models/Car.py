from peewee import *
from models.CarModel import CarModel


class Car(CarModel):
    location = CharField()
    carID = IntegerField(primary_key=True)
