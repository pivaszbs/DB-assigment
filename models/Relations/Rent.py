from peewee import *
from models.BaseModel import BaseModel
from models.Car import Car
from models.Customer import Customer


class Rent(BaseModel):
    username = ForeignKeyField(Customer, backref='driver')
    car = ForeignKeyField(Car, backref='car')