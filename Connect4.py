import requests
import typing

GAME_CONSTANTS = {
    "EMPTY" : 0, #actual value put on board for empty tiles
    "P1" : 1, #actual value put on board for player 1 tiles
    "P2" : -1, #actual value put on board for player 2 tiles
    "REPR_EMPTY" : '_', #what empty tiles look like on board when printed
    "REPR_P1" : 'X', #what player 1 tiles look like on board when printed
    "REPR_P2" : 'Y', #what player 2 tiles look like on board when printed

    "WIDTH" : 7, #board width
    "HEIGHT" : 6, #board height

    "IN_A_ROW" : 4 #to win
}


class Connect4:
    def __init__(self):
        
        #save game constants to object
        self.game_constants = GAME_CONSTANTS
        
        
        #initialize board cells as empty
        board = {}
        for x in range(self.game_constants["WIDTH"]):
            for y in range(self.game_constants["HEIGHT"]):
                board[(x,y)] = self.game_constants["EMPTY"]
        self.board = board

        #how much space in each column
        self.columns = {}
        for x in range(self.game_constants["WIDTH"]):
            self.columns[x] = self.game_constants["HEIGHT"]

        #how much space is left period
        self.space_left = self.game_constants["WIDTH"]*self.game_constants["HEIGHT"]

        #changed by get_winner() when game over
        self.game_over = False

        #changed by get_winner() when game over
        #player 1 win -> 1, player 2 win -> 2
        self.winner = 0

        #player 1 moves first
        self.turn = 1
        return

    def __repr__(self):
        string = "To move: Player " + str(self.to_move) + "\n"
        for y in range(self.game_constants["HEIGHT"]):
            for x in range(self.game_constants["WIDTH"]):
                value = self.board[(x,self.game_constants["HEIGHT"] - y - 1)]

                if value == self.game_constants["EMPTY"]:
                    string += self.game_constants["REPR_EMPTY"] + ' '

                if value == self.game_constants["P1"]:
                    string += self.game_constants["REPR_P1"] + ' '

                if value == self.game_constants["P2"]:
                    string += self.game_constants["REPR_P2"] + ' '

            string += '\n'
        return string
    

    #player goes. Add tile of player in bottom of specified column
    def insert(self, column, tile):
        for dx in range(self.game_constants["WIDTH"]):
            index = (column + dx) % self.game_constants["WIDTH"]

            #is there space at this column?
            if self.columns[index] > 0:

                #add into board
                for y in range(0, self.game_constants["HEIGHT"]):
                    if self.board[(index, y)] == self.game_constants["EMPTY"]:
                        self.board[(index, y)] = tile
                        self.columns[index] -= 1
                        self.space_left -= 1
                        return
                    
    
    #sees if game is over, and modifies self.winner and self.game_over accordingly
    def get_winner(self):

        if self.space_left <= 0:
            self.game_over = True
            self.winner = 0
            return
        
        #test horizontal win condition
        for y in range(0, self.game_constants["HEIGHT"]):
            for x in range(0, self.game_constants["WIDTH"] - self.game_constants["IN_A_ROW"] + 1):
                in_a_row = 0
                for i in range(self.game_constants["IN_A_ROW"]):
                    in_a_row += self.board[(x+i, y)]

                if in_a_row == self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 1
                    return
                if in_a_row == -self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 2
                    return

        #test vertical win condition
        for y in range(0, self.game_constants["HEIGHT"] - self.game_constants["IN_A_ROW"] + 1):
            for x in range(0, self.game_constants["WIDTH"]):
                in_a_row = 0
                for i in range(self.game_constants["IN_A_ROW"]):
                    in_a_row += self.board[(x, y+i)]

                if in_a_row == self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 1
                    return
                if in_a_row == -self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 2
                    return

        #test positive_slope win condition
        for y in range(0, self.game_constants["HEIGHT"] - self.game_constants["IN_A_ROW"] + 1):
            for x in range(0, self.game_constants["WIDTH"] - self.game_constants["IN_A_ROW"] + 1):
                in_a_row = 0
                for i in range(self.game_constants["IN_A_ROW"]):
                    in_a_row += self.board[(x+i, y+i)]

                if in_a_row == self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 1
                    return
                if in_a_row == -self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 2
                    return

        #test negative_slope win condition
        for y in range(0, self.game_constants["HEIGHT"] - self.game_constants["IN_A_ROW"] + 1):
            for x in range(0, self.game_constants["WIDTH"] - self.game_constants["IN_A_ROW"] + 1):
                in_a_row = 0
                for i in range(self.game_constants["IN_A_ROW"]):
                    in_a_row += self.board[(x+i, self.game_constants["IN_A_ROW"]-1 + y-i)]

                if in_a_row == self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 1
                    return
                if in_a_row == -self.game_constants["IN_A_ROW"]:
                    self.game_over = True
                    self.winner = 2
                    return
        
















