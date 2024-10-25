"""
prints current board state
"""
def print_board(board):
  for y in range(len(board)):
    print(board[len(board) - y - 1])

"""
returns move to be made
"""
def get_move(board):
  #TODO: Implement move logic here
  print_board(board)
  
  return 1
