from app.models.user_auth.user_auth import GameUser


def test_home(client):
    response = client.get("/home")
    assert b"<title>Hangman game</title>" in response.data


def test_registration(client, app):
    response = client.post(
        "/register",
        data={
            "name": "testname",
            "email": "test@test.com",
        },
    )

    with app.app_context():
        assert GameUser.query.count() == 1
        assert GameUser.query.first().email == "test@test.com"
