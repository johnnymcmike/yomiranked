import datetime
import random
from elote import EloCompetitor, GlickoCompetitor
from math import sqrt, pi
q = 0.00575646273

def CalculateDrakRank(winner_rating, winner_rd, winner_lastActive, loser_rating,loser_rd,loser_lastActive):
    #winner_LastActive and loser_lastActive are datetime objects
    #calculate the number of seconds between winner last active and now:
    winner_Elapsed = (datetime.datetime.now() - winner_lastActive).total_seconds()
    loser_Elapsed = (datetime.datetime.now() - loser_lastActive).total_seconds()

    newWinR, newWinRD = player1update(winner_rating, winner_rd, winner_Elapsed, loser_rating, loser_rd, loser_Elapsed, 1)
    newLoseR, newLoseRD = player1update(loser_rating, loser_rd, loser_Elapsed, winner_rating, winner_rd, winner_Elapsed, 0)
    return newWinR, newWinRD, newLoseR, newLoseRD


def player1update(player1_r,player1_rd, player1_dt, player2_r,player2_rd,player2_dt,win_or_lose):
    player1_rd = rd_update_before_game(player1_rd,2,player1_dt)
    player2_rd = rd_update_before_game(player2_rd,2,player2_dt)

    g = 1/sqrt(1+((3 * q**2 *player2_rd**2)/(pi**2)))
    E = 1/(1+pow(10,g*(player1_r-player2_r)/(-400)))
    d2 = 1/(q**2 * g**2 * E * (1-E))


    p1_newrating = player1_r + ((q/((1/player1_rd**2) + 1/d2)) * g * (win_or_lose - E))

    p1_newRD = rd_update_after_game(player1_rd,d2)

    return p1_newrating, p1_newRD



def rd_update_after_game(rd,d2):
    return sqrt(((1/rd**2)+(1/d2))**(-1))

def rd_update_before_game(rd,c,t):
    return min(sqrt(rd**2 + t * c**2),350)

#print(player1update(1500, 350, 1, 1000, 350, 1, 1))




def CalculateRankEloNew(winner_rating, loser_rating, k=200):

    expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
    
    expected_loser = 1 / (1 + 10 ** ((winner_rating - loser_rating) / 400))
    
    new_winner_rating = winner_rating + k * (1 - expected_winner)
    new_loser_rating = loser_rating + k * (0 - expected_loser)

    teehee = 0
    if winner_rating == 1250 and loser_rating == 1250:
        teehee = ((random.random() * 5) * random.choice([-1,1])) + random.random()

    if new_winner_rating < 500:
        new_winner_rating = 499
    if new_loser_rating < 500:  
        new_loser_rating = 499
    
    return new_winner_rating + teehee, new_loser_rating + teehee

# Returns a 4 item list. The first 2 are the winner and losers' new GlickoData, the last 2 are their new ratings.
# def CalculateRankGlicko(winnerData, loserData):
#     #player object parameters
#     wData = winnerData.split(",,")
#     lData = loserData.split(",,")
#     winG = GlickoCompetitor(initial_rating=1000)
#     winG.rating = float(wData[0])
#     winG.rd = float(wData[1])
#     winG._c = float(wData[2])
#     winG._q = float(wData[3])
#     loseG = GlickoCompetitor(initial_rating=1000)
#     loseG.rating = float(lData[0])
#     loseG.rd = float(lData[1])
#     loseG._c = float(lData[2])
#     loseG._q = float(lData[3])

#     winG.beat(loseG)

#     winState = winG.export_state()
#     loseState = loseG.export_state()
#     winData = f"{winState['initial_rating']},,{winState['initial_rd']},,{winState['class_vars']['_c']},,{winState['class_vars']['_q']}"
#     loseData = f"{loseState['initial_rating']},,{loseState['initial_rd']},,{loseState['class_vars']['_c']},,{loseState['class_vars']['_q']}"
#     #initial_rating,,initial_rd,,_c,,_q
#     return [winData, loseData, winG.rating, loseG.rating]

# # Returns a list of 2 ints. First one is winner's rating, second one is loser's rating.

# def CalculateRank(winnerRating, loserRating):
#     winner = EloCompetitor(initial_rating= winnerRating)
#     loser = EloCompetitor(initial_rating= loserRating)
#     winner._base_rating = 1000
#     loser._base_rating = 1000
#     winner._k_factor = 64
#     loser._k_factor = 64
#     winner.beat(loser)

#     winResult = winner.rating
#     loseResult = loser.rating

#     if winResult < 500:
#         winResult = 500
#     if loseResult < 500:
#         loseResult = 500
    
#     return [winResult, loseResult]

# def WinProbability(p1rating, p2rating):
#     p1 = EloCompetitor(initial_rating=p1rating)
#     p2 = EloCompetitor(initial_rating=p2rating)
#     return '%5.2f%%' % (p1.expected_score(p2) * 100)
