from app.schema import UserOut
from database import client, session


# create a user
def test_create_user(client):
    res = client.post('/users/', json={"username":"Nightwing", "email":"Dick.Grayson@batfam.inc", "password":"nightwing"})
    new_user = UserOut(**res.json())
    assert res.json().get("username") == new_user.username
    assert res.json().get("email") == new_user.email
