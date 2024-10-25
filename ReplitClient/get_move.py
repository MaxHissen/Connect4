def print_board(board):
  for y in range(len(board)):
    print(board[len(board) - y - 1])

def get_move(board):
  print_board(board)
  
  return 1