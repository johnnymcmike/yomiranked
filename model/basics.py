from peewee import *
db = SqliteDatabase('testing.db',pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db