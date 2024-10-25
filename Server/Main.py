from TestGame import TestGame
from Tournament import RunTournament
import math

#displays the game board after every move
DISPLAY = True

#list of players to add
PLAYER_DICT = {
    "Column5Bot" : "https://connect4-ydyh.onrender.com/",
    "RandomBot" : "https://connect4-1.onrender.com/",
    "CounterBot" : "https://connect4-2.onrender.com/",
    "DummyABPruner" : "https://connect4-tbp7.onrender.com/"
}


"""
TestGame to test your AI.
"""
player_1 = "https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/" #X
player_2 = "https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/" #Y
#TestGame(player_1, player_2, display=DISPLAY)


"""
Tournament
"""
players = []
players.append(PLAYER_DICT["RandomBot"])
players.append(PLAYER_DICT["Column5Bot"])
players.append(PLAYER_DICT["CounterBot"])
players.append(PLAYER_DICT["DummyABPruner"])

#Tournament settings
wins = 4 #first to n wins advances
home_away_schedule = [1,1,0,0,1,0,1] #higher seed goes first if 1


#Round Robin settings
games = 6 #games per player in season. Will be rounded up to nearest even number. Recommended to be a multiple of amount of players
#RunTournament(players_list=players, wins_to_clinch_series=wins, home_away_schedule=home_away_schedule, season_games_amount=games)


