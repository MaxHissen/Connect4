import math
import random
import sys

random.seed(10)

#import player Class
from Player import Player
from Connect4 import Connect4


#constants for printing round robin standings
MAX_NAME_LENGTH = 15
NAME_SPACE = 20

#when printing values (p, w, l, t, gr)
NUMBERS_SPACE = 4

#amount of games each player plays in round robin
GAMES_PER_PLAYER = 6


class Game:
    def __init__(self, home_player, away_player):
        
        #players. home, away
        self.players = [home_player, away_player]
        
        #game completed
        self.completed = False
        
        #game outcome
        #0 - draw
        #1 - home win
        #2 - away win
        self.outcome = None
    
    #play game to completion. Calls bots
    def play(self):
        game = Connect4()
        
        while not game.game_over:

            #get board state to show player in make_move() function
            board_state = {str(key): (-value * (game.turn*2 - 3)) for key, value in game.board.items()}

            move = self.players[game.turn - 1].get_move(board_state)
            
            move_tile = game.game_constants["P1"]
            if game.turn == 2:
                move_tile = game.game_constants["P2"]

            #make move player specified
            game.insert(move, move_tile)

            #test to see if game is over
            game.get_winner()


            #change who's turn to move next
            if game.turn == 1:
                game.turn = 2
            else:
                game.turn = 1
    
        return game.winner
    
    #how game looks when printed
    def __repr__(self):
        string = ""
        string += return_to_print(self.players[1].name, MAX_NAME_LENGTH)
        #if game over
        if self.completed:
            #print arrow in direction of player who won
            if self.outcome == 0:
                string += "  <-|->  "
            elif self.outcome == 1:
                string += "    |--->"
            else:
                string += "<---|    "
        else:
            #no one won yet; game isn't over
            string += "    |    "
            
        string += return_to_print(self.players[0].name, MAX_NAME_LENGTH)
        
        return string

#RoundRobin class. runs round robin then seeds tournament
class RoundRobin:
    def __init__(self, players_list, games_per_player):
        
        #save amount of players
        self.amount_of_players = len(players_list)
        
        if self.amount_of_players <= 1:
            print("Ya need more than 1 player")
            sys.exit()
        
        #list of players to use in round robin
        self.players_list = players_list
        
        #round robin points
        self.points = [0]*self.amount_of_players
        
        #round robin wins
        self.wins = [0]*self.amount_of_players
        #round robin losses
        self.losses = [0]*self.amount_of_players
        #round robin ties
        self.ties = [0]*self.amount_of_players
        
        #round robin games played so far
        self.games_played = [0]*self.amount_of_players
        
        #how many games remaining against each player
        self.games_remaining_per_player = [[0]*self.amount_of_players]*self.amount_of_players
        
        #how many games remaining period
        self.games_remaining = [0]*self.amount_of_players
        
        #get games
        schedule = []
        while games_per_player > 0:
            games_to_schedule_per_player = math.ceil(min(self.amount_of_players - 1, games_per_player/2))
            for x in range(self.amount_of_players):
                for y in range(games_to_schedule_per_player):
                    
                    #find player indeces
                    team1 = x%self.amount_of_players
                    team2 = (y + x + 1)%self.amount_of_players
                    
                    #add 2 games to schedule (one first move other second move)
                    schedule.append(Game(self.players_list[team1], self.players_list[team2]))
                    schedule.append(Game(self.players_list[team2], self.players_list[team1]))
                    
                    #player 1 and 2 have more games remaining now
                    self.games_remaining[team1] += 1
                    self.games_remaining[team2] += 1
                    
                    #player 1 and 2 have more games against eachother now
                    self.games_remaining_per_player[team1][team2] += 1
                    self.games_remaining_per_player[team2][team1] += 1
                    
                    #made games, so reduce amount of games per player
                    games_per_player -= 2/self.amount_of_players
            
            #make sure whole number (eg no rounding errors) 
            games_per_player = round(games_per_player)

        random.shuffle(schedule)

        #list of all games to play
        self.remaining_schedule = schedule


    def __repr__(self):
        string = "Round Robin "
        if len(self.remaining_schedule) > 0:
            string += "In progress."
        else:
            string += "Completed."
        string += '\n\n'
        string += "STANDINGS:\n\n"
        string += "       " + "Name" + "      "
        string += "  " + return_to_print("Pts", NUMBERS_SPACE)
        string += "    " + return_to_print("W", NUMBERS_SPACE)
        string += "   " + return_to_print("L", NUMBERS_SPACE)
        string += "   " + return_to_print("T", NUMBERS_SPACE)
        string += "  " + return_to_print("GR", NUMBERS_SPACE)
        string += "\n"
        
        #sort players by score
        sorted_by_index = sorted(enumerate(self.points), key=lambda x: x[0])
        sorted_scores = [score for index, score in sorted_by_index]
        
        sorted_scores = [0,1,2,3,4,5,6]
        
        for player_id in sorted_scores:
            string += "-"*(NUMBERS_SPACE*4 + MAX_NAME_LENGTH + 3*5 + 6) + "\n|"
            
            player = players_list[player_id]
            #print player stats and stuff
            
            player_name = player.name
            if not player_name:
                player_name = "MISSING DATA"
            string += return_to_print(player_name, MAX_NAME_LENGTH)
            
            string += "| "
            
            #print score next
            player_score = str(self.points[player_id])
            string += return_to_print(player_score, NUMBERS_SPACE)
            
            string += " | "
            
            player_wins = str(self.wins[player_id])
            string += return_to_print(player_wins, NUMBERS_SPACE)
            
            string += " | "
            
            player_losses = str(self.losses[player_id])
            string += return_to_print(player_losses, NUMBERS_SPACE)
            
            string += " | "
            
            player_ties = str(self.ties[player_id])
            string += return_to_print(player_ties, NUMBERS_SPACE)
            
            string += " | "
            
            player_ties = str(self.games_remaining[player_id])
            string += return_to_print(player_ties, NUMBERS_SPACE)
            
            string += " | "
            
            string += "\n"    
        
        string += "-"*(NUMBERS_SPACE*4 + MAX_NAME_LENGTH + 3*5 + 6) + "\n"
            
        return string    

    def play_next_game(self):
        #get next game to play
        next_game = self.remaining_schedule.pop()
        
        #run game to completion and find winner
        winner = next_game.play()
        print(next_game)
        
        #get player ids
        home_player = next_game.players[0].id
        away_player = next_game.players[1].id
        
        print(home_player, away_player)
        
        self.games_remaining[home_player] -= 1
        self.games_remaining[away_player] -= 1
        
        self.games_remaining_per_player[home_player][away_player] -= 1
        self.games_remaining_per_player[away_player][home_player] -= 1
        
        if winner == 0:
            self.ties[home_player] += 1
            self.ties[away_player] += 1
            self.points[home_player] += 1
            self.points[away_player] += 1
        
        if winner == 1:
            self.wins[home_player] += 1
            self.losses[away_player] += 1
            self.points[home_player] += 2
        
        if winner == 2:
            self.wins[away_player] += 1
            self.losses[home_player] += 1
            self.points[away_player] += 2

#returns string, but sets it to target length
def return_to_print(string, target_length):
    # Ensure string is a string
    string = str(string)
    
    if len(string) > target_length:
        return string[:target_length - 3] + "..."
    else:
        return string + " " * (target_length - len(string))


players_list = []
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))
players_list.append(Player("https://36bfd9f0-58b2-439d-9b8c-0d9542714e51-00-30ivmv1v0r0jy.kirk.replit.dev/"))

round_robin = RoundRobin(players_list, GAMES_PER_PLAYER)
print(round_robin)
round_robin.play_next_game()
print(round_robin)
