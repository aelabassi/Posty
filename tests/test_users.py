from app.schema import UserOut, Token
from app.config import settings
from database import client, session
import pytest
from jose import jwt

@pytest.fixture
def test_user(client):
    user_data = {"username": "Robin", "email":"Damian.wyne@batfam.inc", "password":"kingrobin"}
    res = client.post('/users/', json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


# login
def test_login(client, test_user):
    res = client.post('/login', data={"username":test_user["email"], "password":test_user["password"]})
    token = Token(**res.json())
    payload = jwt.decode(token.token, settings.secret_key, settings.algorithm)
    id_ = payload["user_id"]
    assert id_ == test_user["id"]
    assert res.json().get("token") == token.token
    assert res.json().get("token_type") == token.token_type
