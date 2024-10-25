import random
import typing
import ast

from get_move import get_move



# move is called on every turn and returns your next move
# Valid moves are from 0-6
# returns what column to put move in
# game_state: dict. 1 -> my moves, -1 -> opponent moves, 0 -> empty
def move(game_state: typing.Dict) -> int:

    board = [[0]*7 for i in range(6)]
    for key in game_state:
        x,y = ast.literal_eval(key)
        board[int(y)][int(x)] = game_state[key]

    next_move = get_move(board)
    
    print(f"MOVE: {next_move}")
    return {"move": next_move}
    

# TIP: If you open your Connect4 AI URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "TODO",  # TODO: Your Connect4 AI Username
        "name": "TODO",
        "info": "TODO"
    }


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "move": move,
        "info": info
    })
