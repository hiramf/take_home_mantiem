from flask import Flask, session, request
import secrets
from uuid import uuid4
from pydantic import BaseModel


class GuessResponse(BaseModel):
    game_id: str
    incorrectly_guessed_letters: list[str]
    guess_result: dict[str, str]


def create_app():

    app = Flask("WordleClone")
    app.secret_key = secrets.token_hex()

    @app.route("/new_game", methods=["POST"])
    def new_game():
        game_id = uuid4()
        session["game_id"] = game_id
        return {"game_id": game_id} 

    @app.route("/guess", methods=["POST"])
    def guess():
        return GuessResponse(
                game_id = request.json["game_id"],
                incorrectly_guessed_letters=[],
                guess_result={}
            ).dict()

    return app


if __name__ == "__main__":
    create_app()