from elote import EloCompetitor, GlickoCompetitor


# Returns a 4 item list. The first 2 are the winner and losers' new GlickoData, the last 2 are their new ratings.
def CalculateRankGlicko(winnerData, loserData):
    #player object parameters
    wData = winnerData.split(",,")
    lData = loserData.split(",,")
    winG = GlickoCompetitor(float(wData[0]), float(wData[1]))
    winG._c = float(wData[2])
    winG._q = float(wData[3])
    loseG = GlickoCompetitor(float(lData[0]), float(lData[1]))
    loseG._c = float(lData[2])
    loseG._q = float(lData[3])

    winG.beat(loseG)

    winState = winG.export_state()
    loseState = loseG.export_state()
    winData = f"{winState['initial_rating']},,{winState['initial_rd']},,{winState['class_vars']['_c']},,{winState['class_vars']['_q']}"
    loseData = f"{loseState['initial_rating']},,{loseState['initial_rd']},,{loseState['class_vars']['_c']},,{loseState['class_vars']['_q']}"
    #initial_rating,,initial_rd,,_c,,_q
    return [winData, loseData, winG.rating, loseG.rating]

# Returns a list of 2 ints. First one is winner's rating, second one is loser's rating.

def CalculateRank(winnerRating, loserRating):
    winner = EloCompetitor(initial_rating= winnerRating)
    loser = EloCompetitor(initial_rating= loserRating)
    winner._base_rating = 1000
    loser._base_rating = 1000
    winner._k_factor = 64
    loser._k_factor = 64
    winner.beat(loser)

    winResult = winner.rating
    loseResult = loser.rating

    if winResult < 500:
        winResult = 500
    if loseResult < 500:
        loseResult = 500
    
    return [winResult, loseResult]

def WinProbability(p1rating, p2rating):
    p1 = EloCompetitor(initial_rating=p1rating)
    p2 = EloCompetitor(initial_rating=p2rating)
    return '%5.2f%%' % (p1.expected_score(p2) * 100)
