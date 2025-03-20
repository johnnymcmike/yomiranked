from marshmallow import Schema, fields, post_load
from peewee import *
from model.basics import BaseModel, db
import datetime

class Player(object):
    def __init__(self, steamId, discordId, rating, yomicoin=0, banned=False, lastActive=datetime.datetime.now(), steamName="nobody", glickoData="---"):
        self.steamId = steamId
        self.steamHash = str(hash(steamId))
        self.discordId = discordId
        self.yomicoin = yomicoin
        self.banned = banned
        self.rating = rating
        self.lastActive = lastActive
        self.steamName = steamName
        self.glickoData = glickoData
    
    def ToDBObject(self):
        return DbPlayer(
            steamId=self.steamId,
            discordId=self.discordId,
            rating=self.rating,
            glickoData=self.glickoData
        )

class DbPlayer(BaseModel):
    steamId = TextField(unique=True)
    steamHash = TextField(default="empty")
    discordId = TextField(default="none provided")
    yomicoin = IntegerField(default=0)
    banned = BooleanField(default=False)
    rating = IntegerField(default=1250)
    lastActive = DateTimeField(default=datetime.datetime.now)
    steamName = TextField(default="nobody")
    glickoData = TextField(default="---")

class PlayerSchema(Schema):
    steamId = fields.Str()
    steamHash = fields.Str(default="empty")
    discordId = fields.Str(default="none provided")
    yomicoin = fields.Int(default=0)
    banned = fields.Bool(load_default=False, dump_default=False)
    rating = fields.Int(default=1250)
    lastActive = fields.DateTime(default=datetime.datetime.now)
    steamName = fields.Str(default="nobody")
    glickoData = fields.Str(default="---")

    @post_load
    def make_user(self, data, **kwargs):
        return Player(**data)