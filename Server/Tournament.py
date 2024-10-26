import math
import random
import sys

#random.seed(10)

#import player Class
from Player import Player
from Connect4 import Connect4


#constants for printing round robin standings
MAX_NAME_LENGTH = 15
NAME_SPACE = 20

#when printing values (p, w, l, t, gr)
NUMBERS_SPACE = 4


class Game:
    def __init__(self, home_player, away_player, display=False):
        
        #whether to print out the board after every move
        self.display = display
        
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
        self.game = Connect4()
        
        while not self.game.game_over:
            
            if self.display:
                print(self.game)

            #get board state to show player in make_move() function
            board_state = {str(key): (-value * (self.game.turn*2 - 3)) for key, value in self.game.board.items()}

            move = self.players[self.game.turn - 1].get_move(board_state)
            
            move_tile = self.game.game_constants["P1"]
            if self.game.turn == 2:
                move_tile = self.game.game_constants["P2"]

            #make move player specified
            self.game.insert(move, move_tile)

            #test to see if game is over
            self.game.get_winner()


            #change who's turn to move next
            if self.game.turn == 1:
                self.game.turn = 2
            else:
                self.game.turn = 1
    
        self.outcome = self.game.winner
        self.completed = True
        
        if self.display:
            print(self.game)
            
        return self.game.winner
    
    #how game looks when printed
    def __repr__(self):
        string = ""
        if self.players[1].name:  
            string += self.players[1].name.center(MAX_NAME_LENGTH, ' ')
        else:
            string += self.players[1].standin_name.center(MAX_NAME_LENGTH, ' ')
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
            
        if self.players[0].name:  
            string += self.players[0].name.center(MAX_NAME_LENGTH, ' ')
        else:
            string += self.players[0].standin_name.center(MAX_NAME_LENGTH, ' ')
        
        return string

#RoundRobin class. runs round robin then seeds tournament
class RoundRobin:
    def __init__(self, players_list, games_per_player):
        
        print(players_list)
        
        #whether round robin has been finished
        self.complete = False
        
        #save amount of players
        self.amount_of_players = len(players_list)
        
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
        self.games_remaining_per_player = [[0] * self.amount_of_players for _ in range(self.amount_of_players)]
        
        #how many games remaining period
        self.games_remaining = [0]*self.amount_of_players
        
        #get games
        schedule = []
        
        home_games_per_player = math.ceil(games_per_player/2)
        while home_games_per_player > 0:
            home_games_to_schedule_this_round = min(home_games_per_player, self.amount_of_players-1)
            for p in range(self.amount_of_players):
                for i in range(home_games_to_schedule_this_round):
                    #find player indeces
                    team1 = p%self.amount_of_players #home team
                    team2 = (i + p + 1)%self.amount_of_players #away team
                    
                    #add 2 games to schedule (one first move other second move)
                    schedule.append(Game(self.players_list[team1], self.players_list[team2]))
                    
                    #player 1 and 2 have 2 more games remaining now
                    self.games_remaining[team1] += 1
                    self.games_remaining[team2] += 1
                    
                    #player 1 and 2 have more games against eachother now
                    self.games_remaining_per_player[team1][team2] += 1
                    self.games_remaining_per_player[team2][team1] += 1
            home_games_per_player -= home_games_to_schedule_this_round
        
        random.shuffle(schedule)

        #list of all games to play
        self.remaining_schedule = schedule

    #prints round robin standings
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
        sorted_indices = sorted(range(len(self.points)), key=lambda i: -self.points[i] + self.losses[i]*0.01)
        
        for player_id in sorted_indices:
            string += "-"*(NUMBERS_SPACE*4 + MAX_NAME_LENGTH + 3*5 + 6) + "\n|"
            
            player = self.players_list[player_id]
            #print player stats and stuff
            
            if player.name:
                string += return_to_print(player.name, MAX_NAME_LENGTH)
            else:
                string += return_to_print(player.standin_name, MAX_NAME_LENGTH)
            
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
        
        string += "-"*(NUMBERS_SPACE*4 + MAX_NAME_LENGTH + 3*5 + 6)
            
        return string    

    #plays next game in game schedule list
    def play_next_game(self):
        #get next game to play
        next_game = self.remaining_schedule.pop()
        
        #run game to completion and find winner
        winner = next_game.play()
        print(next_game.game)
        print(next_game)
        
        #get player ids
        home_player = next_game.players[0].id
        away_player = next_game.players[1].id
        
        self.games_remaining[home_player] -= 1
        self.games_remaining[away_player] -= 1
        
        self.games_remaining_per_player[home_player][away_player] -= 1
        self.games_remaining_per_player[away_player][home_player] -= 1
        
        if winner == 0:
            self.ties[home_player] += 1
            self.ties[away_player] += 1
            self.points[home_player] += 1
            self.points[away_player] += 1
            self.players_list[home_player].points += 1
            self.players_list[away_player].points += 1
        
        if winner == 1:
            self.wins[home_player] += 1
            self.losses[away_player] += 1
            self.points[home_player] += 2
            self.players_list[home_player].points += 1
        
        if winner == 2:
            self.wins[away_player] += 1
            self.losses[home_player] += 1
            self.points[away_player] += 2
            self.players_list[away_player].points += 1
        
        #if games are over, set complete
        if len(self.remaining_schedule) <= 0:
            self.complete = True
    
    #runs entire round robin to completion, then runs tournament
    def run_round_robin(self):
        
        print(self)
        while not self.complete:
            self.play_next_game()
            print(self)


#Series Class. runs best of (SERIES_CLINCH_GAMES_AMOUNT*2-1) series
#Calls Game
class Series:
    def __init__(self, win_target, home_away):
        
        #updated at player insert. if only one player, bye round
        self.bye = False
        
        #wins to win series
        self.win_target = win_target
        
        #wins per player
        self.wins = [0, 0]
        
        #game number
        self.game = 1
        
        #list of players
        self.players = []
        
        #home vs away schedule
        self.home_away = home_away
    
    def __repr__(self):
        string = ""
        
        if len(self.players) < 2:
            return "Series not set"
        
        if not self.players[0] or not self.players[1]:
            return "Bye Round"
        
        if self.game == 1:
            string += "Series: "
            string += "(" + str(self.players[0].seed) + ")" + return_to_print(self.players[0].name, 10)
            string += " - "
            string += return_to_print(self.players[1].name, 10) + "(" + str(self.players[1].seed) + ")"
            return string
        
        if self.wins[0] < self.win_target and self.wins[1] < self.win_target:
            if self.wins[0] == self.wins[1]:
                string += "Series tied " + str(self.wins[0]) + " - " + str(self.wins[1])
            elif self.wins[0] > self.wins[1]:
                string += self.players[0].name + " leads Series " + str(self.wins[0]) + " - " + str(self.wins[1])
            elif self.wins[1] > self.wins[0]:
                string += self.players[1].name + " leads Series " + str(self.wins[1]) + " - " + str(self.wins[0])
        
        elif self.wins[0] == self.win_target:
            string += self.players[0].name + " wins Series " + str(self.wins[0]) + " - " + str(self.wins[1])
            
        elif self.wins[1] == self.win_target:
            string += self.players[1].name + " wins Series " + str(self.wins[1]) + " - " + str(self.wins[0])
            
        return string
        
    def add_player(self, player):
        
        if len(self.players) >= 2:
            print("too many players in series")
            sys.exit()
        
        #add player to list of players
        self.players.append(player)
    
        #set home vs away
        self.players = sorted(self.players, key=lambda player: (player is None, player.seed if player is not None else None))
        
        #set whether bye round
        amount_of_players = 0
        for player in self.players:
            if player:
                amount_of_players += 1
        self.bye = amount_of_players == 1   
        
    def play_series(self):
        
        if self.players[0] == None:
            return self.players[1]
        if self.players[1] == None:
            return self.players[0]
            
        
        
        while self.wins[0] < self.win_target and self.wins[1] < self.win_target:
            print("")
            input("Play Game " + str(self.game) + ":")
            
            home = self.home_away[self.game - 1] == 1
            game = None
            if home:
                #home game
                game = Game(self.players[0], self.players[1])
            else:
                #road game
                game = Game(self.players[1], self.players[0])
            
            game.display = True
            winner = game.play()
            print(game)
            
            if winner == 1:
                self.wins[1-int(home)] += 1
            elif winner == 2:
                self.wins[int(home)] += 1
            self.game += 1
            
            print(self)
        
        print("")
        input("Continue")
        
        if self.wins[0] >= self.win_target:
            return self.players[0]
        else:
            return self.players[1]

#Tournament Class
class Tournament:
    def __init__(self, round_robin):
        
        #get list of all players sorted by score
        random.shuffle(round_robin.players_list)
        sorted_players = sorted(round_robin.players_list, key=lambda player: -player.points)

        #sorted players
        self.sorted_players = sorted_players
        
        #amount of rounds to win tournament
        self.rounds_amount = math.ceil(math.log2(len(self.sorted_players)))
        self.bracket_space = 2**self.rounds_amount

        seeding = [0] * self.bracket_space

        for i in range(math.ceil(self.bracket_space/2)):
            even_seed = even_seed_from_match_nr(i+1, self.rounds_amount)
            seeding[2*i+1] = even_seed - 1
            seeding[2*i] = self.bracket_space+1-even_seed - 1
        
        bracket = [None for _ in range(len(seeding))]
        for i in range(len(bracket)):
            seed = seeding[i]
            if seed < len(sorted_players):
                self.sorted_players[seed].seed = seed+1
                bracket[i] = self.sorted_players[seed]
        
        self.bracket = bracket
    
    def __repr__(self):
        string = "BRACKET\n"
        
        h_spacing_factor = 45
        
        amount_of_series = len(self.list_of_series)
        amount_of_rounds = self.rounds_amount
        
        line_numbers = [0] * amount_of_series
        
        for round in range(self.rounds_amount):
            for series in range(2**(self.rounds_amount - round - 1)):
                i = round_series_to_index(round, series, amount_of_rounds)
                line_numbers[i] = (2**round) + (2**round)*series*2

        
        for line_number in range(max(line_numbers) + 1):
            line = " "*140
            for round in range(self.rounds_amount):
                for series in range(2**(self.rounds_amount - round - 1)):
                    i = round_series_to_index(round, series, amount_of_rounds)
                    if line_numbers[i] == line_number:
                    
                        index = h_spacing_factor*round
                        round_string = ""
                        series_object = self.list_of_series[i]
                        if len(series_object.players) == 1:
                            round_string += "(" + str(series_object.players[0].seed) + ")" + return_to_print(series_object.players[0].name, 10)
                            round_string += " " + str(series_object.wins[0]) + " - " + str(series_object.wins[1]) + " "
                            round_string += return_to_print("TBD", 10)
                        
                        elif len(series_object.players) == 2:
                            if series_object.players[0] and series_object.players[1]:
                                round_string += "(" + str(series_object.players[0].seed) + ")" + return_to_print(series_object.players[0].name, 10)
                                round_string += " " + str(series_object.wins[0]) + " - " + str(series_object.wins[1]) + " "
                                round_string += return_to_print(series_object.players[1].name, 10) + "(" + str(series_object.players[1].seed) + ")"
                            
                            elif series_object.players[0] and not series_object.players[1]:
                                round_string += "(" + str(series_object.players[0].seed) + ")" + return_to_print(series_object.players[0].name, 10)
                                round_string += return_to_print("BYE", 10)
                            
                            elif not series_object.players[0] and series_object.players[1]:
                                round_string += return_to_print("BYE", 10)
                                round_string += return_to_print(series_object.players[1].name, 10) + "(" + str(series_object.players[1].seed) + ")"
                        
                        else:
                            round_string += "Series Not Determined Yet"
                        line = line[:index] + round_string + line[index:]
            string += line + "\n"
        
        return string
    
    #runs the tournament
    def run_tournament(self, wins_to_win_series, home_away_schedule):
        
        amount_of_matches = math.floor(len(self.bracket)/2)
        
        #all series in tournament
        self.list_of_series = [Series(wins_to_win_series, home_away_schedule) for _ in range(amount_of_matches * 2 - 1)]
        
        #set first rounds series
        for i in range(2**(self.rounds_amount - 1)):
            self.list_of_series[i].add_player(self.bracket[2*i])
            self.list_of_series[i].add_player(self.bracket[2*i + 1])
        
        for self.round in range(self.rounds_amount - 1):
            
            starting_index = 2 ** (self.rounds_amount) - 2 ** (self.rounds_amount - self.round)
            next_round_starting_index = 2 ** (self.rounds_amount) - 2 ** (self.rounds_amount - self.round - 1)
            
            #see if can fill next rounds first
            for i in range(next_round_starting_index - starting_index):
                series = self.list_of_series[starting_index + i]
                child_series = self.list_of_series[next_round_starting_index + math.floor(i/2)]
                is_bye = series.bye

                if is_bye:
                    #add bye player to next round
                    child_series.add_player(series.players[0])
            
            print(self)
            input("\nStart Round" + str(self.round + 1) + ": ")
            
            for i in range(next_round_starting_index - starting_index):
                series = self.list_of_series[starting_index + i]
                child_series = self.list_of_series[next_round_starting_index + math.floor(i/2)]
                if not series.bye:
                    print(self)
                    print("")
                    print(series)
                    input("\nPlay Series:")
                    child_series.add_player(series.play_series())
        
        #championship is the last series
        series = self.list_of_series[-1]
        print(self)
        input("\nStart Final: ")
        print("")
        print(series)
        input("\nPlay Series:")
        champion = series.play_series()
        
        print(self)
        print(champion.name, "Wins the Tournament")
        
        
        
#returns string, but sets it to target length
def return_to_print(string, target_length):
    # Ensure string is a string
    string = str(string)
    
    if len(string) > target_length:
        return string[:target_length - 3] + "..."
    else:
        return " " * math.floor((target_length - len(string))/2) + string + " " * math.floor((target_length - len(string))/2)

#returns index in list series is found in
#r = round
#s = series
#n = number of rounds
def round_series_to_index(r, s, n):
    starting_index = 2 ** (n) - 2 ** (n - r)
    return starting_index + s
    
def even_seed_from_match_nr(i, n): # match_nr, log2(participants)
    #decompose i = 2^k + r where 0 <= r < 2^k
    k = int(math.floor(math.log(i,2)))
    r = i - (1 << k)

    if (r == 0): return 1 << n-k

    nr = bin(i - 2*r)[2:][::-1]
    return int(nr,2) << n-len(nr) | 1 << n-k-1

def RunTournament(players_list, wins_to_clinch_series, home_away_schedule, season_games_amount):
    amount_of_players = len(players_list)
    
    if season_games_amount < 1:
        print("Ya need more than 1 game per player")
    
    if amount_of_players <= 1:
        print("Ya need more than 1 player")
        sys.exit()
            
    #make sure that home_away_schedule length = max_series_length
    if wins_to_clinch_series*2-1 != len(home_away_schedule):
        print("series wins needs to be same length as home-away schedule")
        sys.exit()
    
    for num in home_away_schedule:
        if num != 1 and num != 0:
            print(num + "in home-away schedule must be 1 or 0")
            sys.exit()
    
    
    #run round robin
    player_objects_list = []
    for i in range(amount_of_players):
        player_objects_list.append(Player(players_list[i]))
        player_objects_list[i].id = i
        
    round_robin = RoundRobin(player_objects_list, games_per_player=season_games_amount)
    round_robin.run_round_robin()
    
    #get input to start tournament
    input("Press Enter To Run Tournament")
    
    #run tournament
    tournament = Tournament(round_robin=round_robin)
    tournament.run_tournament(wins_to_clinch_series, home_away_schedule)
