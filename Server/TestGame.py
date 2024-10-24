from Player import Player
from Tournament import Game

"""
Used to test a game
"""

def TestGame(link1, link2, display=False):
    player1 = Player(link1)
    player2 = Player(link2)
    
    game = Game(player1, player2, display)
    outcome = game.play()
    
    print(game)