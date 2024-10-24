from marshmallow import Schema, fields, post_load
from peewee import *
from model.basics import BaseModel, db
import datetime

#i'm not really sure whether having the database classes and the Player/Match classes separate makes any sense
#if any smart code people are reading this feel free to suggest improvements
#i'll accept PRs lol
class Player(object):
    def __init__(self,  steamId, discordId, rating, lastActive = datetime.datetime.now(),steamName = "nobody"):
        self.steamId = steamId
        self.steamHash = str(hash(steamId))
        self.discordId = discordId
        self.rating = rating
        self.lastActive = lastActive
        self.steamName = steamName
    
    def ToDBObject(self):
        return DbPlayer(
            steamId=self.steamId,
            discordId=self.discordId,
            rating=self.rating
        )

class DbPlayer(BaseModel):
    steamId = TextField(unique=True)
    steamHash = TextField(unique=True, default="empty")
    discordId = TextField(default="none provided")
    rating = IntegerField(default=1000)
    lastActive = DateTimeField(default=datetime.datetime.now)
    steamName = TextField(default="nobody")

class PlayerSchema(Schema):
    steamId = fields.Str()
    steamHash = fields.Str(default="empty")
    discordId = fields.Str(default="none provided")
    rating = fields.Int(default=1000)
    lastActive = fields.DateTime(default=datetime.datetime.now)
    steamName = fields.Str(default="nobody")

    @post_load
    def make_user(self, data, **kwargs):
        return Player(**data)