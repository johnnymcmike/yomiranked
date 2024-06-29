from flask import Flask, jsonify, request
from model.match import *
from model.player import *
from model.basics import db
from rating.rank import CalculateRank
from marshmallow import ValidationError
from peewee import *

app = Flask(__name__)

@app.route('/test')
def test():
    return "hello from yomiranked!"

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    amount = request.args.get('amount', default=10, type=int)
    playerList = DbPlayer.select(DbPlayer.steamId).order_by(DbPlayer.rating.desc()).limit(amount)
    list = []
    schema = PlayerSchema()
    for player in playerList:
        list.append(schema.dump(player))
    

    return jsonify(list), 200

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
    knownMatch = DbMatch.get_or_none(dbMatch.rngSeed)

    if knownMatch:
        if knownMatch.confirmed == True:
            db.close()
            return jsonify("duplicate report, match already confirmed."), 400
        else:
            #match confirmation
            knownMatch.confirmed = True
            knownMatch.save()

            winner, wcreated = DbPlayer.get_or_create(steamId=knownMatch.winner_steamId)
            loser, lcreated = DbPlayer.get_or_create(steamId=knownMatch.loser_steamId)
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

        winner, wcreated = DbPlayer.get_or_create(steamId=dbMatch.winner_steamId)
        loser, lcreated = DbPlayer.get_or_create(steamId=dbMatch.loser_steamId)
        newRatings = CalculateRank(winner.rating, loser.rating)
        #we read the DB for rating, but do NOT write anything, when we recieve an unconfirmed match
        winnerHypotheticalRating = round(newRatings[0])
        loserHypotheticalRating = round(newRatings[1])
        db.close()

        results = {
                "!msg": "match resgistered, but not yet confirmed. here are the potential ratings",
                "winnerNewRating": winnerHypotheticalRating,
                "loserNewRating": loserHypotheticalRating,
            }
        
        return jsonify(results),202



@app.route('/getsecret', methods=['GET'])
def getsecret():
    return "not yet implemented"