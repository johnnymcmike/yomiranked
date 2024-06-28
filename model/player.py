from marshmallow import Schema, fields
from peewee import *
from model.basics import BaseModel, db
import datetime

class Player(object):
    def __init__(self,  steamId, discordId, rating, lastActive = datetime.datetime.now()):
        self.steamId = steamId
        self.discordId = discordId
        self.rating = rating
        self.lastActive = lastActive
    
    def ToDBObject(self):
        return ModeledPlayer(
            steamId=self.steamId,
            discordId=self.discordId,
            rating=self.rating
        )

class ModeledPlayer(BaseModel):
    steamId = CharField(primary_key=True)
    discordId = CharField()
    rating = IntegerField()
    lastActive = DateTimeField(default=datetime.datetime.now)

class PlayerSchema(Schema):
    steamId = fields.Str()
    discordId = fields.Str(default="none provided")
    rating = fields.Int(default=1000)
    lastActive = fields.DateTime(default=datetime.datetime.now)