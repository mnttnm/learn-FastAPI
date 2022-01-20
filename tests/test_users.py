from app import schemas
from app.config import settings
import pytest
from jose import jwt


# def test_root(client):
#     res = client.get('/')
#     assert res.json().get("message") == "Welcome"


# we use /users/ and not /users as for /users the server redirects us to /users/ with the res
# code as 307 and our status code assertion will fail
# this is because we are using /users prefix in our routes
def test_create_user(client):
    res = client.post("/users/", json={
        "email": "test1@gmail.com",
        "password": "test123"
    })

    new_user = schemas.UserOut(**res.json())
    assert (new_user.email == "test1@gmail.com")
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user['email'],
        "password": test_user['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wronemail@gmail.com", "test123", 403),
    ("test_user@gmail.com", "incorrect_password", 403),
    (None, "test123", 422),
    ("test_user@gmail.com", None, 422)
])
def test_invalid_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })
    assert res.status_code == status_code
