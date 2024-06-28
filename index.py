from flask import Flask, jsonify, request

from model.match import *
from model.player import *
from model.basics import db
from rating.rank import WinProbability, CalculateRank

from marshmallow import ValidationError
from peewee import *

app = Flask(__name__)

@app.route('/test')
def test():
    return "hello from yomiranked!"

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    return "example string"

#JSON body for this one
@app.route('/gamereport', methods=['POST'])
def gamereport():
    try:
        data = request.get_json()
        schema = MatchSchema()
        match = schema.load(data)
    except ValidationError as err:
        return ["There was a problem with the format of the request.",err.messages], 400

    db.connect()
    dbMatch = match.ToDBObject()
    knownMatch = ModeledMatch.get_or_none(dbMatch.rngSeed)

    if knownMatch:
        if knownMatch.confirmed == True:
            db.close()
            return jsonify("duplicate report, match already confirmed."), 400
        else:
            knownMatch.confirmed = True
            knownMatch.save()

            winner = ModeledPlayer.get_or_create(knownMatch.winner_steamId)
            loser = ModeledPlayer.get_or_create(knownMatch.loser_steamId)

            newRatings = CalculateRank(winner.rating, loser.rating)
            winner.rating = newRatings[0]
            loser.rating = newRatings[1]
            


            db.close()
            return jsonify("match confirmed!"), 200
    else:
        dbMatch.save(force_insert=True)
        db.close()
        return jsonify("match registered!"),200



@app.route('/getsecret', methods=['GET'])
def getsecret():
    return "secret"

@app.route('/signup', methods=['POST'])
def signup():
    return "example string"