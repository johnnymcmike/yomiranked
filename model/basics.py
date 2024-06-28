from peewee import *
db = SqliteDatabase('testing.db')

class BaseModel(Model):
    class Meta:
        database = db