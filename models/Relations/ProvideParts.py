from peewee import *
from models.BaseModel import BaseModel
from models.Provider import Provider
from models.WorkShop import Workshop

class ProvideParts(BaseModel):
    provider = ForeignKeyField(Provider)
    workshop = ForeignKeyField(Workshop)