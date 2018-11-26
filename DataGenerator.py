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
from models.Events.TripEvent import TripEvent
from models.Events.RepairingEvent import RepairingEvent
from models.Events.ChargingEvent import ChargingEvent


def generate_car():
    i = ri(0, 10)
    colour = ["red", "white", "blue", "green", "yellow", "black", "brown", "orange", "pink", "gray"]
    mark = ["Tesla", "HipsterCar", "Lambargingi", "LADA", "BMW",
            "Audi", "Mersedes", "YoYoMobil", "SashaGrayCar", "ElectroZaporozhec"]

    plate = ''
    plate += chr(ord('A') + ri(0, 25))
    plate += chr(ord('A') + ri(0, 25))

    for i in range(4):
        plate += chr(ord('0') + ri(0, 9))

    name = mark[ri(0, len(mark) - 1)] + "Special electic edition " + str(i)
    power = ri(50, 500)
    color = colour[ri(0, len(colour) - 1)]
    location = [str(i) + "room" for i in range(100, 131)]
    loc = location[ri(0, 30)]
    Car.create(location=loc, name=name, power=power, color=color, plate=plate)


def generate_provider():
    names = ["ElectroSosiskaCompany", "WunderWaflya", "SOS",
             "TeslaCommunity", "ElectroSamolet", "Energizer", "RazRazIGotovo",
             "BestCarFriend", "Lighting", "The drift of the soul"]
    name = names[ri(0, len(names) - 1)]
    phone_number = "880055" + (str(ri(2, 9) * 10) + "5") * 2
    Provider.create(name=name, phone_number=phone_number)


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
                        residential_address=ResidentialAddress.get_by_id(ri(1, ResidentialAddress.select().count())),
                        email=email,
                        full_name=names[ri(0, len(names) - 1)])
    except:# KeyError as error:
        username += str(ri(0, 9999999))
        email = username + "@" + domains[ri(0, len(domains) - 1)]
        Customer.create(phone_number=phone_number, username=username,
                        residential_address=ResidentialAddress.get_by_id(ri(1, ResidentialAddress.select().count())),
                        email=email,
                        full_name=names[ri(0, len(names) - 1)])


def generate_residential_address():
    countries = ["Russia", "Africa", "America", "TrampsCountry",
                 "PutinsCountry", "China", "World", "England", "Germany", "USSR"]
    cities = ["Vladivostok", "Moscow", "PutinGrad", "KimChenIn", "EmeraldCity",
              "Dzen", "SPB", "Innopolis", "Gorod", "Zelenodolsk"]
    ResidentialAddress.create(country=countries[ri(0, len(countries) - 1)],
                              city=cities[ri(0, len(cities) - 1)])


def generate_charging_station():
    gpsx = random() * 1000
    gpsy = random() * 1000
    price_of_charging = ri(100, 3000)
    time_of_charging = datetime.timedelta(seconds=randrange(50, 300)).seconds
    available_sockets = ri(15, 100)
    ChargingStation.create(GPSx=gpsx, GPSy=gpsy, price_of_charging=price_of_charging,
                           time_of_charging=time_of_charging, available_sockets=available_sockets)


def generate_socket():
    plugs = ["US", "UA", "UL", "USB", "TYPECC", "GJJ",
             "STACK", "LULZ"]
    sizes = [12, 24, 36, 48, 60]
    size = sizes[ri(0, len(sizes) - 1)]
    Socket.create(plug_type=plugs[ri(0, len(plugs) - 1)] + "-" + str(size), plug_size=size)


def generate_workshop():
    availability_of_timing = datetime.timedelta(hours=randrange(100, 500))
    Workshop.create(availability_of_timing=availability_of_timing)


def generate_trip_event():
    pickup_time = datetime.datetime(year=ri(2015, 2018), month=ri(1, 12), day=ri(1, 28), hour=ri(0, 23), minute=ri(0, 59), second=ri(0, 59))
    end_time = (pickup_time + datetime.timedelta(hours=int(ri(1, 1000))))
    location = [str(i) + " street" for i in range(100, 131)]
    pickup_location = location[ri(0, 30)]
    destination_location = location[ri(0, 30)]
    TripEvent.create(pickup_location=pickup_location, pickup_time=pickup_time, end_time=end_time,
                     destination_location=destination_location, car=Car.get_by_id(
            ri(1, Car.select().count())),
                     customer=Customer.get_by_id(ri(1, Customer.select().count())))


def generate_repairing_event():
    time = datetime.datetime(year=ri(2000, 2018), month=ri(1, 12), day=ri(1, 28), hour=ri(0, 23), minute=ri(0, 59),
                             second=ri(0, 59))
    RepairingEvent.create(time=time, customer=Customer.get_by_id(ri(1, Customer.select().count())),
                          workshop=Workshop.get_by_id(ri(1, Workshop.select().count())), car=Car.get_by_id(
            ri(1, Car.select().count())))


def generate_charging_event():
    time = datetime.datetime(year=ri(2000, 2018), month=ri(1, 12), day=ri(1, 28), hour=ri(0, 23), minute=ri(0, 59),
                             second=ri(0, 59))
    ChargingEvent.create(time=time, car=Car.get_by_id(ri(1, Car.select().count())),
                         customer=Customer.get_by_id(ri(1, Customer.select().count())),
                         charging_station=ChargingStation.get_by_id(ri(1, ChargingStation.select().count())))
