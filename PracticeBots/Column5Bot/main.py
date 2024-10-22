import random
import typing

def move(game_state: typing.Dict) -> int:
    next_move = 4

    print(f"MOVE: {next_move}")
    return {"move": next_move}
    

def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "Snoblaxx",
        "name": "Column5Bot",
        "info": "This bot really likes the number 5"
    }


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "move": move,
        "info": info
    })
