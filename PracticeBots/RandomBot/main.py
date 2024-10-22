import random
import typing

def move(game_state: typing.Dict) -> int:
    next_move = random.randint(0,6)

    return {"move": next_move}
    

def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "Snoblaxx",
        "name": "RandomBot",
        "info": "This bot is blind. Makes random moves"
    }


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "move": move,
        "info": info
    })
