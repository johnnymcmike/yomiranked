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
            #match confirmation
            knownMatch.confirmed = True
            knownMatch.save()

            print(knownMatch.winner_steamId, knownMatch.loser_steamId)
            winner, wcreated = ModeledPlayer.get_or_create(steamId=knownMatch.winner_steamId)
            loser, lcreated = ModeledPlayer.get_or_create(steamId=knownMatch.loser_steamId)
            newRatings = CalculateRank(winner.rating, loser.rating)
            winner.rating = round(newRatings[0])
            loser.rating = round(newRatings[1])
            winner.lastActive = datetime.datetime.now()
            loser.lastActive = datetime.datetime.now()
            winner.save()
            loser.save()

            results = {
                "!msg": "match confirmed! here are the new ratings",
                "winnerNewRating": winner.rating,
                "loserNewRating": loser.rating,
            }
            db.close()
            return jsonify(results), 200
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