from fastapi.testclient import TestClient
from app.config import settings
from app.database import Base, get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


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
