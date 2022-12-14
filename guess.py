from dataclasses import dataclass
from pydantic import BaseModel


WORD_OF_THE_DAY = "CROWN"


@dataclass
class GameSession:
    game_id: str
    attempts: int = 0
    answer: str = WORD_OF_THE_DAY
    solved = False


class GuessResult(BaseModel):
    game_id: str
    incorrectly_guessed_letters: list
    results: dict


class Game:
    def __init__(self, session: dict):
        self.game_id: str = session["game_id"]
        self.session: dict = session
        self.answer: str = session["answer"]

    def process_guess(self, guess: str) -> GuessResult:
        # assumes len(guess) == len(answer)
        incorrectly_guessed_letters = []
        guess_result = "correct"
        letters = {}

        for i in range(len(self.answer)):
            if guess[i] == self.answer[i]:
                letters[f"letter{i+1}"] = "correct"
            else:
                guess_result = "incorrect"
                if guess[i] in self.answer:
                    letters[f"letter{i+1}"] = "wrong_position"
                else:
                    letters[f"letter{i+1}"] = "incorrect"
                    incorrectly_guessed_letters.append(guess[i])

        return {
            "game_id": self.game_id,
            "guess_result": guess_result,
            "incorrectly_guessed_letters": incorrectly_guessed_letters
        } | letters
    
    def __dict__(self):
        return {
            "game_id": self.game_id,
            "attempts:": self.attempts,
        }