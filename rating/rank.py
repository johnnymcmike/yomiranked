from elote import EloCompetitor

# Returns a list of 2 ints. First one is winner's rating, second one is loser's rating.
def CalculateRank(winnerRating, loserRating):
    winner = EloCompetitor(initial_rating= winnerRating)
    loser = EloCompetitor(initial_rating= loserRating * 0.95)
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
