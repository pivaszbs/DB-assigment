from peewee import *
from models.BaseModel import BaseModel
from models.WorkShop import Workshop
from models.Car import Car
from models.Customer import Customer


class Repairing(BaseModel):
    workshop = ForeignKeyField(Workshop)
    car = ForeignKeyField(Car)
    customer = ForeignKeyField(Customer)