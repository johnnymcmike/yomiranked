from flask import Flask, jsonify, request
from model.match import *
from model.player import *
from model.basics import db
from rating.rank import CalculateRank
from marshmallow import ValidationError
from peewee import *
import requests

app = Flask(__name__)
#probably bad practice to use one db connection but it's causing weird issues
db.connect()
steamApiKey = ""
with open('steamApiKey.txt', 'r') as file:
    steamApiKey = file.read().replace('\n', '')

@app.route('/')
def index():
    return "hello from yomiranked!"

@app.route('/test')
def test():
    return "hello from yomiranked!"

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    #db.connect()
    amount = request.args.get('amount', default=10, type=int)
    playerList = DbPlayer.select().order_by(DbPlayer.rating.desc()).limit(amount)
    #i'm not really a python guy so there may be a cooler, shorter way to do this part
    #i know c# could do this in one line with linq
    #lmk if you know anything
    list = []
    schema = PlayerSchema()
    for player in playerList:
        list.append(schema.dump(player))
    #db.close()
    return jsonify(list), 200

#need JSON body for this one
@app.route('/gamereport', methods=['POST'])
def gamereport():
    try:
        data = request.get_json()
        schema = MatchSchema()
        match = schema.load(data)
    except ValidationError as err:
        return ["There was a problem with the format of the request.",err.messages], 400

    #db.connect()
    dbMatch = match.ToDBObject()
    knownMatch = DbMatch.get_or_none(dbMatch.rngSeed)

    if knownMatch != None:
        if knownMatch.confirmed == True:
            #db.close()
            return jsonify("duplicate report, match already confirmed."), 400
        else:
            #match confirmation
            knownMatch.confirmed = True
            knownMatch.save()

            #need to assign it like this bc that function returns a tuple
            winner = getOrCreatePlayer(knownMatch.winner_steamId)
            loser = getOrCreatePlayer(knownMatch.loser_steamId)
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
            #db.close()
            return jsonify(results), 200
    else:
        dbMatch.save(force_insert=True) #this param is required because we have a custom private key

        winner = getOrCreatePlayer(dbMatch.winner_steamId)
        loser = getOrCreatePlayer(dbMatch.loser_steamId)
        newRatings = CalculateRank(winner.rating, loser.rating)
        #we read the DB for rating, but do NOT write anything, when we recieve an unconfirmed match
        winnerHypotheticalRating = round(newRatings[0])
        loserHypotheticalRating = round(newRatings[1])
        #db.close()

        results = {
                "!msg": "match resgistered, but not yet confirmed. here are the potential ratings",
                "winnerNewRating": winnerHypotheticalRating,
                "loserNewRating": loserHypotheticalRating,
            }
        
        return jsonify(results),202



@app.route('/getrank', methods=['GET'])
def getrank():
    playerId = request.args.get('player', default=-1, type=int)
    if playerId == -1:
        return jsonify("no player specified"), 400
    else:
        #db.connect()
        player = getOrCreatePlayer(playerId)
        #db.close()
        return jsonify(player.rating), 200

@app.route('/debugMatches', methods=['GET'])
def debugMatches():
    data = DbMatch.select()
    list = []
    schema = MatchSchema()
    for match in data:
        list.append(schema.dump(match))
    #db.close()
    return jsonify(list), 200


#helper functions
def getOrCreatePlayer(desiredSteamId):
    #we assume that db is already connected here
    player, created = DbPlayer.get_or_create(steamId=desiredSteamId)
    if created:
        response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamApiKey}&steamids={desiredSteamId}").json()
        if(response):
            player.steamName = response["response"]["players"][0]["personaname"]
    
    player.save()

    #db.close()
    return player
