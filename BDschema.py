from peewee import *

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
    CMID = IntegerField(unique=True)
    name = CharField()
    power = IntegerField()


class Car(CarModel):
    Location = CharField()
    CarID = IntegerField(unique=True)


class Provider(BaseModel):
    name = CharField()
    phone_number = CharField()
    companyID = PrimaryKeyField()


class Customer(BaseModel):
    phone = CharField()
    email = CharField()
    country = CharField()
    city = CharField()
    zip = IntegerField()
    username = CharField(unique=True)
    full_name = CharField()


class ChargingStation(BaseModel):
    GPS = IntegerField()  # IDKrightnow
    price_of_charging = IntegerField()
    CSUID = IntegerField(unique=True)
    time_of_charging = TimeField()
    available_sockets = IntegerField()


class Socket(BaseModel):
    plug_type = CharField()
    plug_size = IntegerField()


class Workshop(BaseModel):
    availabilty_of_timing = TimeField()
    WID = IntegerField()


class Charging(BaseModel):
    CarID = ForeignKeyField(Car, backref='charging_car')
    # It's just relation
    plug_type = ForeignKeyField(Socket, field='plug_type')
    plug_size = ForeignKeyField(Socket, field='plug_size')


class Rent(BaseModel):
    username = ForeignKeyField(Customer, backref='driver')
    car = ForeignKeyField(Car, backref='car')


class Repairing(BaseModel):
    pass


class ProvideParts(BaseModel):
    pass


def create_tables():
    with db:
        db.create_tables([Charging, Socket, Workshop, Charging, ChargingStation,
                          Customer, Provider, Car, Rent, Repairing, ProvideParts])
