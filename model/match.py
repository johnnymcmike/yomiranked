from marshmallow import Schema, fields, post_load
from uuid import uuid4
from peewee import *
from model.basics import BaseModel, db
import datetime

#i'm not really sure whether having the database classes and the Player/Match classes separate makes any sense
#if any smart code people are reading this feel free to suggest improvements
#i'll accept PRs lol

class Match(object):
    def __init__(self,  rngSeed, winner_steamId, loser_steamId, confirmed = False, timestamp = datetime.datetime.now()):
        self.rngSeed = rngSeed
        self.winner_steamId = winner_steamId
        self.loser_steamId = loser_steamId
        self.timestamp = timestamp
        self.confirmed = confirmed
    
    def ToDBObject(self):
        return DbMatch(
            rngSeed=self.rngSeed,
            winner_steamId=self.winner_steamId,
            loser_steamId=self.loser_steamId,
            timestamp=self.timestamp
        )

class DbMatch(BaseModel):
    rngSeed = IntegerField(primary_key=True)
    winner_steamId = CharField()
    loser_steamId = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    confirmed = BooleanField(default=False)


class MatchSchema(Schema):
    rngSeed = fields.Integer()
    winner_steamId = fields.Str()
    loser_steamId = fields.Str()
    timestamp = fields.DateTime()
    confirmed = fields.Boolean(load_default = False, dump_default = False)

    @post_load
    def make_user(self, data, **kwargs):
        return Match(**data)