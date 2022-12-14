import pytest
from app import GuessResponse, create_app

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


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()


def test_new_game(client):
    response = client.post("/new_game")
    assert response.json["game_id"]

def test_guess(client):
    response = client.post("/guess", json={"game_id": 123})
    guess_response = GuessResponse(**response.json)