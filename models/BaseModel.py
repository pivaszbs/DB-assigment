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