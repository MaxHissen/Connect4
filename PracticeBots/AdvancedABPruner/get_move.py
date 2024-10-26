import sys
import math
import random

class Position:
  def __init__(self, board):
    self.board = board

    #start with player X to play
    self.turn = 0

    #depth of position in search
    self.search_depth = 0

    #history of moves made in position while minimax to undo later
    self.move_history = []

    #is state terminal. is win-loss-draw
    self.terminal = False

  #print position
  def __repr__(self):
    string = "----Position----\n"
    string += "To move: "
    if self.turn == 1:
      string += "X"
    else:
      string += "Y"
    
    string += "\n"

    #print search depth
    string += "Depth: " + str(self.search_depth) + "\n"
    #print move history
    string += "Move history: "
    for i in range(len(self.move_history)):
      string += "Move " + str(i) + ": " + str(self.move_history[i]) + ", "
    if len(self.move_history) > 0:
      string = string[:-2]
    else:
      string += "None"
    string += "\n"
    
    for y in range(len(self.board)):
      for x in range(len(self.board[y])):
        value = self.board[len(self.board) - y - 1][x]
        if value == 0:
          string += "_"
        elif value == 1:
          string += "X"
        else:
          string += "Y"
        string += " "
      string += "\n"
    string += "\n"

    return string

  #make move on position. Updates depth and move history
  def make_move(self, column):

    made_move = False
    
    #find lowest empty space in column
    for i in range(6):
      if self.board[i][column] == 0:
        if self.turn == 0:
          self.board[i][column] = 1
        else:
          self.board[i][column] = -1
        made_move = True
        break

    if made_move:
      #switch turn
      self.turn = (self.turn + 1) % 2
      self.move_history.append(column)
      self.search_depth += 1

    else:
      print("make move error")
      print(self)
      print(column)
      sys.exit()

  #unmake the most recent move. Updates depth and move history
  def unmake_move(self):
  
    unmade_move = False

    column = self.move_history.pop()
  
    #find lowest empty space in column
    for i in range(6):
      if self.board[5-i][column] != 0:
        self.board[5-i][column] = 0
        unmade_move = True
        break
  
    if unmade_move:
      #switch turn
      self.turn = (self.turn + 1) % 2
      self.search_depth -= 1

      if self.search_depth < 0:
        print("search depth below 0")
        print(self)
        print(column)
        sys.exit()
  
    else:
      print("unmake move error")
      print(self)
      print(column)
      sys.exit()

  #returns a list of legal moves
  def get_moves(self):
    moves = []
    for i in range(7):
      if self.board[5][i] == 0:
        moves.append(i)
    return moves

  def get_ordered_moves(self):
    move_ordering = [math.inf * -int(self.turn == 0)]*7
    moves = self.get_moves()
    for move in moves:
      self.make_move(move)
      move_ordering[move] = self.static_evaluation()
      self.unmake_move()

    #order moves
    # Create a list of tuples (move, score)
    moves_with_scores = [(move, move_ordering[move]) for move in moves]

    # Sort the moves based on their score
    sorted_moves = sorted(moves_with_scores, key=lambda x: -int(self.turn != 0)*x[1])

    # Extract the sorted moves
    sorted_moves_list = [move for move, score in sorted_moves]

    return sorted_moves_list

  #returns whether the game is over and no more moves will be made
  def is_terminal(self):

    if len(self.get_moves()) <= 0:
      return True

    #test horizontal win condition
    for y in range(0, 6):
      for x in range(0, 7 - 4 + 1):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[y][x+i]

        if abs(in_a_row) == 4:
          return True

    #test vertical win condition
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[y+i][x]

        if abs(in_a_row) == 4:
          return True

    #test positive_slope win condition
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7 - 4 + 1):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[y+i][x+i]

        if abs(in_a_row) == 4:
          return True

    #test negative_slope win condition
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7 - 4 + 1):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[4-1 + y-i][x+i]

        if abs(in_a_row) == 4:
          return True

    return False
    
  #returns the evaluation for a terminal position
  #inf for win, #-inf for loss, 0 for draw
  def terminal_evaluation(self):
    
    if len(self.get_moves()) <= 0:
      return 0

    #test horizontal win condition
    for y in range(0, 6):
      for x in range(0, 7 - 4 + 1):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[y][x+i]

        if in_a_row == 4:
          return math.inf
        if in_a_row == -4:
          return -math.inf

    #test vertical win condition
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[y+i][x]

        if in_a_row == 4:
          return math.inf
        if in_a_row == -4:
          return -math.inf

    #test positive_slope win condition
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7 - 4 + 1):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[y+i][x+i]

        if in_a_row == 4:
          return math.inf
        if in_a_row == -4:
          return -math.inf

    #test negative_slope win condition
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7 - 4 + 1):
        in_a_row = 0
        for i in range(4):
          in_a_row += self.board[4-1 + y-i][x+i]

        if in_a_row == 4:
          return math.inf
        if in_a_row == -4:
          return -math.inf
          
  #TODO
  #returns the evaluation of a non-terminal position
  def static_evaluation(self):


    
    #get all empty cells that can finish a 3 in a row with a 1 or -1
    me_gaps = [[0]*7 for i in range(6)]
    enemy_gaps = [[0]*7 for i in range(6)]
    
    #horizontal
    for y in range(0, 6):
      for x in range(0, 7 - 4 + 1):
        amount = 0
        is_a_gap = None
        for i in range(4):
          x_pos = x+i
          y_pos = y
          value = self.board[y_pos][x_pos]
          amount += value
          if value == 0:
            is_a_gap = (x_pos, y_pos)

        if is_a_gap:
          if amount == 3:
            me_gaps[is_a_gap[1]][is_a_gap[0]] = 1
          elif amount == -3:
            enemy_gaps[is_a_gap[1]][is_a_gap[0]] = 1
          
    #positive
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7 - 4 + 1):
        amount = 0
        is_a_gap = None
        for i in range(4):
          x_pos = x+i
          y_pos = y+i
          value = self.board[y_pos][x_pos]
          amount += value
          if value == 0:
            is_a_gap = (x_pos, y_pos)

        if is_a_gap:
          if amount == 3:
            me_gaps[is_a_gap[1]][is_a_gap[0]] = 1
          elif amount == -3:
            enemy_gaps[is_a_gap[1]][is_a_gap[0]] = 1

    #negative
    for y in range(0, 6 - 4 + 1):
      for x in range(0, 7 - 4 + 1):
        amount = 0
        is_a_gap = None
        for i in range(4):
          x_pos = x+i
          y_pos = 4-1 + y-i
          value = self.board[y_pos][x_pos]
          amount += value
          if value == 0:
            is_a_gap = (x_pos, y_pos)

        if is_a_gap:
          if amount == 3:
            me_gaps[is_a_gap[1]][is_a_gap[0]] = 1
          elif amount == -3:
            enemy_gaps[is_a_gap[1]][is_a_gap[0]] = 1

    single_gaps = [0, 0]
    for x in range(7):
      for y in range(6):
        if me_gaps[y][x] == 1:
          single_gaps[0] += 1
        if enemy_gaps[y][x] == 1:
          single_gaps[1] += 1

    double_gaps = [0, 0]
    for x in range(7):
      for y in range(5):
        if me_gaps[y][x] == 1 and me_gaps[y+1][x] == 1:
          double_gaps[0] += 1
        if enemy_gaps[y][x] == 1 and enemy_gaps[y+1][x] == 1:
          double_gaps[1] += 1

    score = (single_gaps[0] - single_gaps[1])*1 + (double_gaps[0] - double_gaps[1])*10
    return score
    
def get_move(board):
  initial_position = Position(board)

  depth_limit = 6
  
    
  
  #iterate through all possible initial moves and get score of each
  move_scores = [-math.inf]*7
  for move in initial_position.get_moves():
    initial_position.make_move(move)
    #run minimax with alpha beta pruning on position after inital move
    move_scores[move] = alpha_beta(initial_position, depth_limit, -math.inf, math.inf)
    initial_position.unmake_move()
  
  #find and return best move
  highest_score = max(move_scores)
  max_indices = [index for index, score in enumerate(move_scores) if score == highest_score]
  random_index = random.choice(max_indices)
  
  
  return random_index

def alpha_beta(cur_position, depth_limit, alpha, beta):
  # Base case
  if cur_position.is_terminal():
    return cur_position.terminal_evaluation()

  if cur_position.search_depth >= depth_limit:
    return cur_position.static_evaluation()

  
  # Recursive case
  
  if cur_position.turn == 0:
    # Maximizing player
    best_score = -math.inf
    for move in cur_position.get_ordered_moves():
        cur_position.make_move(move)
        score = alpha_beta(cur_position, depth_limit - 1, alpha, beta)
        cur_position.unmake_move()
        best_score = max(best_score, score)
        alpha = max(alpha, best_score)  # Update alpha
        if alpha >= beta:  # Prune the remaining branches
          break
  else:
    # Minimizing player
    best_score = math.inf
    for move in cur_position.get_ordered_moves():
      cur_position.make_move(move)
      score = alpha_beta(cur_position, depth_limit - 1, alpha, beta)
      cur_position.unmake_move()
      best_score = min(best_score, score)
      beta = min(beta, best_score)  # Update beta
      if alpha >= beta:  # Prune the remaining branches
        break

  return best_score
