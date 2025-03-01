from app.schema import Token
from app.config import settings
from jose import jwt
import pytest

# login
def test_login(client, test_user):
    res = client.post('/login', data={"username": test_user["email"], "password": test_user["password"]})
    token = Token(**res.json())
    payload = jwt.decode(token.token, settings.secret_key, settings.algorithm)
    id_ = payload["user_id"]
    assert id_ == test_user["id"]
    assert res.json().get("token") == token.token
    assert res.json().get("token_type") == token.token_type

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "kingrobin", 403),
    ("Damian.wyne@batfam.inc", "wrongpassord", 403),
    ("stephanie.brown@batfam.inc", "Steph", 403),
    (None, "password123", 422),
    ("Cassandra.kane@batfam.inc", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password":password})
    assert res.status_code == status_code