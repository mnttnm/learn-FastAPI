# all the modules under the parent package of this conftest file will have access to the fixture defined here.
from fastapi.testclient import TestClient
from app.config import settings
from app.database import Base, get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.oauth2 import create_access_token

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # for every API request a session is established with dbms and then
# # once the request is done, the session is terminated
# # Dependency


@pytest.fixture()
def session():
    # drop all the tables so that we start with a clean slate
    Base.metadata.drop_all(bind=engine)
    # create tables before running the tests
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test_user@gmail.com",
        "password": "test123"
    }
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data.get('password')
    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    token = create_access_token({"user_id": test_user["id"]})
    return token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
