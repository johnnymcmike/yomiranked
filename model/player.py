from marshmallow import Schema, fields, post_load
from peewee import *
from model.basics import BaseModel, db
import datetime

#i'm not really sure whether having the database classes and the Player/Match classes separate makes any sense
#if any smart code people are reading this feel free to suggest improvements
#i'll accept PRs lol
class Player(object):
    def __init__(self,  steamId, discordId, rating, lastActive = datetime.datetime.now()):
        self.steamId = steamId
        self.discordId = discordId
        self.rating = rating
        self.lastActive = lastActive
    
    def ToDBObject(self):
        return DbPlayer(
            steamId=self.steamId,
            discordId=self.discordId,
            rating=self.rating
        )

class DbPlayer(BaseModel):
    steamId = CharField(primary_key=True)
    discordId = CharField(default="none provided")
    rating = IntegerField(default=1000)
    lastActive = DateTimeField(default=datetime.datetime.now)

class PlayerSchema(Schema):
    steamId = fields.Str(primary_key=True)
    discordId = fields.Str(default="none provided")
    rating = fields.Int(default=1000)
    lastActive = fields.DateTime(default=datetime.datetime.now)

    @post_load
    def make_user(self, data, **kwargs):
        return Player(**data)