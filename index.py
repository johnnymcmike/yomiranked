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

@app.route('/gethash')
def gethash():
    input = request.args.get('id', default="0", type=str)
    if len(input) >= 20:
        return jsonify("too long"), 400
    return jsonify(hash(input)), 200

@app.route('/registerdiscord', methods=['POST'])
def registerdiscord():
    #takes in a steamHash and a discordId, searches the database for a matching steamHash, and updates the discordId
    #db.connect()
    data = request.get_json(force=True)
    steamHash = data["steamHash"]
    discordId = data["discordId"]
    player = DbPlayer.get_or_none(DbPlayer.steamHash == steamHash)
    if player == None:
        #db.close()
        return jsonify("no player found with that steamHash"), 400
    else:
        player.discordId = discordId
        player.save()
        #db.close()
        return jsonify("discord id updated"), 200

@app.route('/test')
def test():
    return "hello from yomiranked!"

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    #db.connect()
    startPlace = request.args.get('start', default=0, type=int)
    endPlace = request.args.get('end', default=24, type=int)


    playerList = DbPlayer.select().where(DbPlayer.rating != 1000).order_by(DbPlayer.rating.desc())
    if endPlace > len(playerList):
        endPlace = len(playerList)
    if startPlace > endPlace:
        return jsonify("invalid range bro"), 400
    goodIndices = list(range(startPlace, endPlace))
    subsetList = [playerList[i] for i in goodIndices]

    #i'm not really a python guy so there may be a cooler, shorter way to do this part
    #i know c# could do this in one line with linq
    #lmk if you know anything
    newlist = []
    schema = PlayerSchema()
    for player in subsetList:
        newlist.append(schema.dump(player))
    #db.close()
    return jsonify(newlist), 200

#need JSON body for this one
@app.route('/gamereport', methods=['POST'])
def gamereport():
    try:
        data = request.get_json(force=True)
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
    playerId = request.args.get('player', default="-1", type=str)
    if playerId == "-1":
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
    response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamApiKey}&steamids={desiredSteamId}").json()
    if(response):
        player.steamName = response["response"]["players"][0]["personaname"]
    player.steamHash = str(hash(desiredSteamId))
    player.save()

    #db.close()
    return player
