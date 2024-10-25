from marshmallow import Schema, fields, post_load
from uuid import uuid4
from peewee import *
from model.basics import BaseModel, db
import datetime

#i'm not really sure whether having the database classes and the Player/Match classes separate makes any sense
#if any smart code people are reading this feel free to suggest improvements
#i'll accept PRs lol

class Match(object):
    def __init__(self,  rngSeed, winner_steamId, loser_steamId, winner_eloBefore, winner_eloAfter, loser_eloBefore, loser_eloAfter, confirmed = False, timestamp = datetime.datetime.now()):
        self.rngSeed = rngSeed
        self.winner_steamId = winner_steamId
        self.winner_eloBefore = winner_eloBefore
        self.winner_eloAfter = winner_eloAfter
        self.loser_steamId = loser_steamId
        self.loser_eloBefore = loser_eloBefore
        self.loser_eloAfter = loser_eloAfter
        self.timestamp = timestamp
        self.confirmed = confirmed
    
    def ToDBObject(self):
        return DbMatch(
            rngSeed=self.rngSeed,
            winner_steamId=self.winner_steamId,
            winner_eloBefore = self.winner_eloBefore,
            winner_eloAfter = self.winner_eloAfter,
            loser_steamId=self.loser_steamId,
            loser_eloBefore = self.loser_eloBefore,
            loser_eloAfter = self.loser_eloAfter,
            timestamp=self.timestamp,
            confirmed = self.confirmed
        )

class DbMatch(BaseModel):
    rngSeed = IntegerField(primary_key=True)
    winner_steamId = TextField()
    winner_eloBefore = IntegerField(default=0000)
    winner_eloAfter = IntegerField(default=0000)
    loser_steamId = TextField()
    loser_eloBefore = IntegerField(default=0000)
    loser_eloAfter = IntegerField(default=0000)
    timestamp = DateTimeField(default=datetime.datetime.now)
    confirmed = BooleanField(default=False)


class MatchSchema(Schema):
    rngSeed = fields.Integer()
    winner_steamId = fields.Str()
    winner_eloBefore = fields.Int()
    winner_eloAfter = fields.Int()
    loser_steamId = fields.Str()
    loser_eloBefore = fields.Int()
    loser_eloAfter = fields.Int()
    timestamp = fields.DateTime()
    confirmed = fields.Boolean(load_default = False, dump_default = False)

    @post_load
    def make_user(self, data, **kwargs):
        return Match(**data)