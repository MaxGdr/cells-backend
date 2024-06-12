from sqlalchemy.orm import Session
from contextlib import ExitStack
from typing import Generator
from db.database import engine, create_all, drop_all
import pytest
from fastapi.testclient import TestClient
from app import app as fastapi_app


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield fastapi_app


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture(scope="function", autouse=True)
def create_tables():
    drop_all(engine)
    create_all(engine)


@pytest.fixture()
def user_header(client: TestClient):
    username: str = "test@example.com"
    password: str = "password"

    response = client.post(
        "/api/v1/users/signup",
        json={"full_name": "Full Name Test", "email": username, "password": password},
    )
    response = client.post(
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        url="/api/v1/login/access-token",
        data={"username": username, "password": password},
    )
    user_creds = response.json()
    return {"Authorization": f"Bearer {user_creds["access_token"]}"}
