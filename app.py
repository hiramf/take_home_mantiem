from dataclasses import dataclass
from flask import Flask, session, request
import secrets
from uuid import uuid4
from pydantic import BaseModel

from guess import Game, GameSession




def create_app():

    app = Flask("WordleClone")
    app.secret_key = secrets.token_hex()

    @app.route("/new_game", methods=["POST"])
    def new_game():
        game_id = str(uuid4())
        session[game_id] = GameSession(game_id=game_id)
        return {"game_id": game_id} 

    @app.route("/guess", methods=["POST"])
    def guess():
        game_id = request.json["game_id"]
        
        if game_id in session:
            game_session = session[game_id]
            game_session["attempts"] += 1
            session.modified = True
        else:
            return "Game not found", 404

        if game_session["attempts"] > 6:
            return "MAX ATTEMPTS REACHED", 400   
            
        game = Game(session=game_session)
        result = game.process_guess(request.json["word"].upper())
        return result



    return app


if __name__ == "__main__":
    create_app()