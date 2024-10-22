import logging
import os
import typing

from flask import Flask
from flask import request


def run_server(handlers: typing.Dict):
    app = Flask("Connect4")

    @app.get("/")
    def on_info():
        return handlers["info"]()

    @app.post("/move")
    def on_move():
        game_state = request.get_json()
        return handlers["move"](game_state)

    @app.after_request
    def identify_server(response):
        response.headers.set(
            "server", "connect4/replit/starter-bot-python"
        )
        return response

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print(f"\nRunning Connect4 at http://{host}:{port}")
    app.run(host=host, port=port)
