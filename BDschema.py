from peewee import *
from numpy.random import random_integers as ri
from numpy.random import random
from random import randrange
import datetime

db = SqliteDatabase('car_share.db', pragmas=(
    ('cache_size', -16000),  # 16MB
    ('journal_mode', 'wal'),  # Use write-ahead-log journal mode.
))

# Alternatively, pragmas can be specified using a dictionary.
db = SqliteDatabase('car_share.db', pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    class Meta:
        database = db


class CarModel(BaseModel):
    CMID = IntegerField(primary_key=True)
    name = CharField()
    power = IntegerField()
    color = CharField()


class ResidentialAddress(BaseModel):
    country = CharField()
    city = CharField()
    zip = IntegerField(primary_key=True)


class Car(CarModel):
    location = CharField()
    carID = IntegerField(primary_key=True)


def generate_random_car():
    i = ri(0, 10)
    colour = ["red", "white", "blue", "green", "yellow", "black", "brown", "orange", "pink", "gray"]
    mark = ["Tesla", "HipsterCar", "Lambargingi", "LADA", "BMW",
            "Audi", "Mersedes", "YoYoMobil", "SashaGrayCar", "ElectroZaporozhec"]

    name = mark[ri(0, len(mark) - 1)] + "Special electic edition " + str(i)
    power = ri(50, 500)
    color = colour[ri(0, len(colour) - 1)]
    location = [str(i) + "room" for i in range(100, 131)]
    loc = location[ri(0, 30)]
    Car.create(location=loc, name=name, power=power, color=color)


class Provider(BaseModel):
    name = CharField()
    phone_number = CharField()
    companyID = PrimaryKeyField()


def generate_provider():
    names = ["ElectroSosiskaCompany", "WunderWaflya", "SOS",
             "TeslaCommunity", "ElectroSamolet", "Energizer", "RazRazIGotovo",
             "BestCarFriend", "Lighting", "The drift of the soul"]
    name = names[ri(0, len(names) - 1)]
    phone_number = "880055" + (str(ri(2, 9) * 10) + "5") * 2
    Provider.create(name=name, phone_number=phone_number)


class Customer(BaseModel):
    phone = CharField()
    email = CharField(unique=True)
    residential_address = ForeignKeyField(ResidentialAddress, field='zip')
    username = CharField(primary_key=True)
    full_name = CharField()


def generate_customer():
    phone_number = "899988" + str(ri(1000, 9999))
    usernames = ["schoolboy", "fatherofyourson", "sweetygirl", "neighbors_grandmother",
                 "killer", "superchill", "manofman", "superscalar", "greatestguy"]
    domains = ["yandex.ru", "mail.ru", "gmail.ru"]
    username = usernames[ri(0, len(usernames) - 1)]
    email = username + "@" + domains[ri(0, len(domains) - 1)]
    names = ["Jon", "Yak", "Bob", "Mo", "Ivan", "Lucifer", "Manyak", "Serdol", "Sanek", "Christopher"]
    try:
        Customer.create(phone_number=phone_number, username=username,
                        email=email, name=names[ri(0, len(names) - 1)])
    except KeyError as error:
        username += str(ri(0, 9999999))
        email = username + "@" + domains[ri(0, len(domains) - 1)]
        Customer.create(phone_number=phone_number, username=username,
                        email=email, name=names[ri(0, len(names) - 1)])


def generate_residential_address():
    countries = ["Russia", "Africa", "America", "TrampsCountry",
                 "PutinsCountry", "China", "World", "England", "Germany", "USSR"]
    cities = ["Vladivostok", "Moscow", "PutinGrad", "KimChenIn", "EmeraldCity",
              "Dzen", "SPB", "Innopolis", "Gorod", "Zelenodolsk"]
    ResidentialAddress.create(country=countries[ri(0, len(countries) - 1)],
                             city=cities[ri(0, len(cities) - 1)])


class ChargingStation(BaseModel):
    GPSx = FloatField()  # IDKrightnow
    GPSy = FloatField()
    price_of_charging = IntegerField()
    CSUID = IntegerField(primary_key=True)
    time_of_charging = TimeField()
    available_sockets = IntegerField()


def generate_charging_station():
    gpsx = random() * 1000
    gpsy = random() * 1000
    price_of_charging = ri(100, 3000)
    time_of_charging = datetime.timedelta(seconds=randrange(50, 300)).seconds
    available_sockets = ri(15, 100)
    ChargingStation.create(GPSx=gpsx, GPSy=gpsy, price_of_charging=price_of_charging,
                           time_of_charging=time_of_charging, available_sockets=available_sockets)


class Socket(BaseModel):
    plug_type = CharField()
    plug_size = IntegerField()


def generate_socket():
    plugs = ["US", "UA", "UL", "USB", "TYPECC", "GJJ",
             "STACK", "LULZ"]
    sizes = [12, 24, 36, 48, 60]
    size = sizes[ri(0, len(sizes) - 1)]
    Socket.create(plug_type=plugs[ri(0, len(plugs) - 1)] + "-" + str(size), plug_size=size)


class Workshop(BaseModel):
    availabilty_of_timing = TimeField()
    WID = IntegerField(primary_key=True)


def generate_workshop():
    availability_of_timing = datetime.timedelta(hours=randrange(100, 500))
    Workshop.create(availability_of_timing=availability_of_timing)


class Charging(BaseModel):
    CarID = ForeignKeyField(Car, backref='charging_car')
    # It's just relation
    plug_type = ForeignKeyField(Socket, field='plug_type')
    plug_size = ForeignKeyField(Socket, field='plug_size')


class Rent(BaseModel):
    username = ForeignKeyField(Customer, backref='driver')
    car = ForeignKeyField(Car, backref='car')


class Repairing(BaseModel):
    workshop = ForeignKeyField(Workshop)
    car = ForeignKeyField(Car)
    customer = ForeignKeyField(Customer)


class ProvideParts(BaseModel):
    provider = ForeignKeyField(Provider)
    workshop = ForeignKeyField(Workshop)


class Event(BaseModel):
    event_id = IntegerField(primary_key=True)
    type = CharField()
    customer = ForeignKeyField(Customer)
    workshop = ForeignKeyField(Workshop)
    start_time = datetime()
    end_time = datetime()
    pickup_location = FloatField() # TODO: create class location ?
    destination_location = FloatField()


def create_tables():
    with db:
        db.create_tables([Charging, Socket, ResidentialAddress, Workshop, Charging, ChargingStation,
                          Customer, Provider, Car, Rent, Repairing, ProvideParts, Event])


def execute_queries():
    cursor = db.cursor()
    f = open("queries.txt")
    for query in f.readlines():
        print(*cursor.execute(query))

#create_tables()
generate_random_car()
execute_queries()