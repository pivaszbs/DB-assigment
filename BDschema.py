from peewee import *
from numpy.random import random_integers as ri
from numpy.random import random
from random import randrange
import datetime
from models.Car import Car
from models.Provider import Provider
from models.Customer import Customer
from models.ResidentalAddress import ResidentialAddress
from models.ChargingStation import ChargingStation
from models.Socket import Socket
from models.WorkShop import Workshop
from models.Relations.Charging import Charging
from models.Relations.ProvideParts import ProvideParts
from models.Relations.Repairing import Repairing
from models.BaseModel import db
from models.Events.ChargingEvent import ChargingEvent
from models.Events.RepairingEvent import RepairingEvent
from models.Events.TripEvent import TripEvent
import DataGenerator


def create_tables():
    with db:
        db.create_tables([Charging, Socket, ResidentialAddress, Workshop, ChargingStation,
                          Customer, Provider, Car, Repairing, ProvideParts, ChargingEvent, RepairingEvent, TripEvent])


def execute_queries():
    cursor = db.cursor()
    f = open("queries.txt")
    for query in f.readlines():
        print(*cursor.execute(query))


create_tables()
DataGenerator.generate_car()
DataGenerator.generate_workshop()
DataGenerator.generate_socket()
DataGenerator.generate_residential_address()
DataGenerator.generate_provider()
DataGenerator.generate_customer()
DataGenerator.generate_charging_station()
#execute_queries()