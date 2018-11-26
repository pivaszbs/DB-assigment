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
        locations = cursor.execute(str(
            'SELECT pickup_location, count(pickup_location) FROM tripevent WHERE CAST(strftime(\'%H\', pickup_time) AS INT) >= ' + str(
                time_from) + ' AND CAST(strftime(\'%H\', pickup_time) AS INT) < ' + str(
                time_to) + ' GROUP BY pickup_location ORDER BY count(pickup_location) DESC LIMIT 3'))
        for loc in locations:
            print(loc[0] + ' (' + str(loc[1]) + ' times)')

        print('\nTop-3 destination locations:')
        locations = cursor.execute(str(
            'SELECT destination_location, count(destination_location) FROM tripevent WHERE CAST(strftime(\'%H\', pickup_time) AS INT) >= ' + str(
                time_from) + ' AND CAST(strftime(\'%H\', pickup_time) AS INT) < ' + str(
                time_to) + ' GROUP BY destination_location ORDER BY count(destination_location) DESC LIMIT 3'))
        for loc in locations:
            print(loc[0] + ' (' + str(loc[1]) + ' times)')

        print('\n')


'''QUERY 7'''


def query_show_10_percent_of_less_used_cars():
    cursor = db.cursor()
    cursor.execute('create table table1 (car_id integer,counter integer)')
    cursor.execute(
        'insert into table1 SELECT car_id, 0 AS counter FROM car WHERE car_id NOT IN ( SELECT car_id FROM (SELECT car_id, count(car_id) FROM tripevent WHERE datetime(pickup_time, \'+2 years\') >= datetime(\'now\') GROUP BY car_id))')
    cursor.execute(
        'insert into table1 SELECT car_id, count(car_id) as counter FROM tripevent WHERE datetime(pickup_time, \'+2 years\') >= datetime(\'now\') GROUP BY car_id')
    data = cursor.execute('select * FROM table1 ORDER BY counter LIMIT (select count(*) from table1) / 10')
    for d in data:
        print('car id: ' + str(d[0]) + '(used ' + str(d[1]) + ' times)')
    cursor.execute('DROP TABLE IF EXISTS table1')



'''QUERY 1'''
def query_1():
    cursor = db.cursor()
    data = cursor.execute('select car_id from car WHERE color=\'red\' and plate like \'OI%\'')
    print('Car Id\'s:')
    for id in data:
        print(id[0])

'''QUERY 2'''
def query_2(date):
    cursor = db.cursor()
    data = cursor.execute('SELECT strftime(\'%H\', time) || \'h-\' || strftime(\'%H\', time(time, \'+1 hour\')) || \'h: \' || count(*) from chargingevent WHERE DATE(time) = \'' + str(date) + '\' GROUP BY strftime(\'%H\', time)')
    for d in data:
        print(d[0])

create_tables()

for i in range(500):
    DataGenerator.generate_trip_event()
# execute_queries()

<<<<<<< HEAD
# query_top_3_popular_locations_for_evety_time_slot()
# query_show_10_percent_of_less_used_cars
=======
#query_1()
query_2('2018-05-01')
#query_top_3_popular_locations_for_evety_time_slot()
#query_show_10_percent_of_less_used_cars
>>>>>>> 8f097a8c6001d1199751510628e1a7419e342528
