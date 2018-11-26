from peewee import *
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


'''QUERY 6'''
def query_top_3_popular_locations_for_evety_time_slot():
    cursor = db.cursor()
    time_slots = [(7, 10), (12, 14), (17, 19)]
    text_time_slots = ['Morning(9AM-10AM)', 'Afternoon(12AM-2PM)', 'Evening(5PM-7PM)']

    for time_slot in range(3):
        print('--------' + text_time_slots[time_slot] + '--------')
        print('Top-3 pickup locations:')
        time_from = time_slots[time_slot][0]
        time_to = time_slots[time_slot][1]
        locations = cursor.execute(str('SELECT pickup_location, count(pickup_location) FROM tripevent WHERE CAST(strftime(\'%H\', pickup_time) AS INT) >= ' + str(time_from) + ' AND CAST(strftime(\'%H\', pickup_time) AS INT) < ' + str(time_to) + ' GROUP BY pickup_location ORDER BY count(pickup_location) DESC LIMIT 3'))
        for loc in locations:
            print(loc[0] + ' (' + str(loc[1]) + ' times)')

        print('\nTop-3 destination locations:')
        locations = cursor.execute(str('SELECT destination_location, count(destination_location) FROM tripevent WHERE CAST(strftime(\'%H\', pickup_time) AS INT) >= ' + str(time_from) + ' AND CAST(strftime(\'%H\', pickup_time) AS INT) < ' + str(time_to) + ' GROUP BY destination_location ORDER BY count(destination_location) DESC LIMIT 3'))
        for loc in locations:
            print(loc[0] + ' (' + str(loc[1]) + ' times)')

        print('\n')




create_tables()

DataGenerator.generate_car()
DataGenerator.generate_workshop()
DataGenerator.generate_socket()
DataGenerator.generate_residential_address()
DataGenerator.generate_provider()
DataGenerator.generate_customer()
DataGenerator.generate_charging_station()
DataGenerator.generate_trip_event()
DataGenerator.generate_repairing_event()
DataGenerator.generate_charging_event()
# execute_queries()

query_top_3_popular_locations_for_evety_time_slot()