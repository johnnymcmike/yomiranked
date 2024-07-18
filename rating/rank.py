from elote import EloCompetitor

# Returns a list of 2 ints. First one is winner's rating, second one is loser's rating.
def CalculateRank(winnerRating, loserRating):
    winner = EloCompetitor(initial_rating= winnerRating * 1.13)
    loser = EloCompetitor(initial_rating= loserRating * 0.87)
    winner.beat(loser)
    
    return [winner.rating, loser.rating]

def WinProbability(p1rating, p2rating):
    p1 = EloCompetitor(initial_rating=p1rating)
    p2 = EloCompetitor(initial_rating=p2rating)
    return '%5.2f%%' % (p1.expected_score(p2) * 100)
