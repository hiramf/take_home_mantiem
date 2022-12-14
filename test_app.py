import pytest
from app import create_app
from guess import GuessResult


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_new_game(client):
    response = client.post("/new_game")
    assert response.json["game_id"]


def test_guess_game_not_found(client):
    response = client.post("/guess", json={"game_id": 123})
    assert response.status_code == 404


def test_guess_game_found(client):
    game_id = client.post("/new_game").json["game_id"]
    response = client.post("/guess", json={"game_id": game_id, "word": "APPLE"}).json
    assert response["game_id"] == game_id


def test_multiple_game_sessions(client):
    game_id_a = client.post("/new_game").json["game_id"]
    game_id_b = client.post("/new_game").json["game_id"]
    response = client.post("/guess", json={"game_id": game_id_a, "word": "crown"}).json
    assert response["game_id"] == game_id_a
    response = client.post("/guess", json={"game_id": game_id_b, "word": "crown"}).json
    assert response["game_id"] == game_id_b


def test_guess_correct(client):
    game_id = client.post("/new_game").json["game_id"]
    guess = "crown"
    response = client.post("/guess", json={"game_id": game_id, "word": guess}).json
    assert "correct" == response["guess_result"]
    assert game_id == response["game_id"]
    for i in range(len(guess)):
        assert response[f"letter{i+1}"] == "correct"


def test_guess_incorrect(client):
    game_id = client.post("/new_game").json["game_id"]
    guess = "crowd"
    response = client.post("/guess", json={"game_id": game_id, "word": guess}).json
    assert "incorrect" == response["guess_result"]
    assert game_id == response["game_id"]
    assert response["incorrectly_guessed_letters"] == ["D"]
    for i in range(len(guess) - 1):
        assert response[f"letter{i+1}"] == "correct"
    assert response["letter5"] == "incorrect"


def test_guess_wrong_position(client):
    game_id = client.post("/new_game").json["game_id"]
    guess = "crown"
    guess = "nwcro"
    response = client.post("/guess", json={"game_id": game_id, "word": guess}).json
    assert "incorrect" == response["guess_result"]
    assert game_id == response["game_id"]
    for i in range(len(guess)):
        assert response[f"letter{i+1}"] == "wrong_position"


def test_max_attempts(client):
    game_id = client.post("/new_game").json["game_id"]
    guess = "crowd"
    for i in range(6):
        client.post("/guess", json={"game_id": game_id, "word": guess}).json

    response = client.post("/guess", json={"game_id": game_id, "word": guess})
    assert response.text == "MAX ATTEMPTS REACHED"
    assert response.status_code == 400
