from marshmallow import Schema, fields, post_load
from uuid import uuid4
from peewee import *
from model.basics import BaseModel, db
import datetime

class Match(object):
    def __init__(self,  rngSeed, winner_steamId, loser_steamId, timestamp = datetime.datetime.now()):
        self.rngSeed = rngSeed
        self.winner_steamId = winner_steamId
        self.loser_steamId = loser_steamId
        self.timestamp = timestamp
    
    def ToDBObject(self):
        return ModeledMatch(
            rngSeed=self.rngSeed,
            winner_steamId=self.winner_steamId,
            loser_steamId=self.loser_steamId,
            timestamp=self.timestamp
        )

class ModeledMatch(BaseModel):
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

    @post_load
    def make_user(self, data, **kwargs):
        return Match(**data)