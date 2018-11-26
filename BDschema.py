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
from models.Part import Part


def create_tables():
    with db:
        db.create_tables([Charging, Socket, ResidentialAddress, Workshop, ChargingStation,
                          Customer, Provider, Car, Repairing, ProvideParts, ChargingEvent, RepairingEvent, TripEvent, Part])


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


def query_5(date):
    cursor = db.cursor()
    data = cursor.execute('select cast(AVG(distance_to_user) as INT) as [Average distance(m)],  cast(AVG(trip_duration)'
                          'as int) as [Average trip duration (min)] from tripevent where date(pickup_time)=' + str(
        date))
    for d in data:
        print(d)


def query_2(date):
    cursor = db.cursor()
    data = cursor.execute(
        'SELECT strftime(\'%H\', time) || \'h-\' || strftime(\'%H\', time(time, \'+1 hour\')) || \'h: \' || count(*) from chargingevent WHERE DATE(time) = \'' + str(
            date) + '\' GROUP BY strftime(\'%H\', time)')
    for d in data:
        print(d[0])


def query_4(username):
    cursor = db.cursor()
    data = cursor.execute('SELECT count(time) as acts, charging_station_id, car_id, residential_address_id, time,'
                          'customer.username FROM customer JOIN chargingevent'
                          ' on customer.c_id = chargingevent.customer_id'
                          'where username = ' + str(username) + ' GROUP BY time HAVING count(time)>1;')
    for d in data:
        print(d[0])


'''QUERY 3'''


def query_3():
    cursor = db.cursor()
    data = cursor.execute('SELECT Morning, Afternoon, Evening '
                          'FROM ( SELECT count(*) * 100 / (SELECT count(*) FROM car) AS \'Morning\' '
                          'FROM tripevent WHERE (CAST(strftime(\'%H\', pickup_time) AS INT) >= 7 AND '
                          'CAST(strftime(\'%H\', pickup_time) AS INT) < 10) OR (CAST(strftime(\'%H\', end_time) AS INT)'
                          ' >= 7 AND CAST(strftime(\'%H\', end_time) AS INT) < 10)), '
                          '(SELECT count(*) * 100 / (SELECT count(*) FROM car) AS \'Afternoon\' FROM tripevent '
                          'WHERE (CAST(strftime(\'%H\', pickup_time) AS INT) >= 12 AND CAST(strftime(\'%H\', pickup_time)' \
                          ' AS INT) < 14) OR (CAST(strftime(\'%H\', end_time) AS INT) >= 12 '
                          'AND CAST(strftime(\'%H\', end_time) AS INT) < 14)), (SELECT count(*) * 100 / (SELECT count(*)'
                          ' FROM car) AS \'Evening\' FROM tripevent WHERE (CAST(strftime(\'%H\', pickup_time) AS INT) ' \
                          '>= 17 AND CAST(strftime(\'%H\', pickup_time) AS INT) < 19) OR ' \
                          '(CAST(strftime(\'%H\', end_time) AS INT) >= 17 AND CAST(strftime(\'%H\', end_time) AS INT) < 19))')
    for d in data:
        for i in range(3):
            print(data.description[i][0])
            print(d[i])
            print()



'''QUERY 9'''
def query_9():
    cursor = db.cursor()
    workshops = cursor.execute('SELECT WID FROM workshop')
    for w in workshops:
        workshop_id = w[0]
        data = cursor.execute('SELECT part_id, count(part_id) FROM ( SELECT * FROM repairingevent WHERE workshop_id = 3) GROUP BY part_id ORDER BY part_id DESC LIMIT 1')
        for d in data:
            most_popular_part_id = d[0]
            most_popular_part = Part.get_by_id(most_popular_part_id).name
            count_per_week = d[1] / 52
            print('Workshop with id ' + str(workshop_id) + ' most often requires' + most_popular_part + '(about ' + str(count_per_week) + ' every week on average)')
            break



create_tables()

#for i in range(100):
DataGenerator.generate_car()
DataGenerator.generate_workshop()
DataGenerator.generate_socket()
DataGenerator.generate_residential_address()
DataGenerator.generate_part()
DataGenerator.generate_provider()
DataGenerator.generate_customer()
DataGenerator.generate_charging_station()
DataGenerator.generate_trip_event()
DataGenerator.generate_repairing_event()
DataGenerator.generate_charging_event()

