import random
import typing



# move is called on every turn and returns your next move
# Valid moves are from 0-6
# returns what column to put move in
# game_state: dict of 1 = my moves, -1 = opponent moves, 0 = empty
def move(game_state: typing.Dict) -> int:

    # TODO: Implement move logic here
    next_move = 3


    
    print(f"MOVE: {next_move}")
    return {"move": next_move}
    

# TIP: If you open your Connect4 AI URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "Snoblaxx",  # TODO: Your Connect4 AI Username
        "name": "Column4Bot",
        "info": "This bot really likes the number 4"
    }


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "move": move,
        "info": info
    })
