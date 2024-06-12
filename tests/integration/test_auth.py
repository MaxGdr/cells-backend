from fastapi.testclient import TestClient
import jwt
import pytest
from core.config import settings


def test_user_can_login(client: TestClient):
    response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "test@example.com",
            "full_name": "Full Name Test",
            "password": "password",
        },
    )
    assert response.status_code == 200

    user = response.json()

    response = client.post(
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        url="/api/v1/login/access-token",
        data={"username": user["email"], "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_valid_jwt_token(client: TestClient):
    response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "test@example.com",
            "full_name": "Full Name Test",
            "password": "password",
        },
    )
    assert response.status_code == 200
    user = response.json()
    response = client.post(
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        url="/api/v1/login/access-token",
        data={"username": user["email"], "password": "password"},
    )
    data = response.json()

    # Extract the access token from the response
    access_token = data["access_token"]

    # Verify the JWT token
    decoded_token = jwt.decode(
        access_token, key=settings.HASH_SECRET_KEY, algorithms=["HS256"]
    )
    assert decoded_token["sub"] == str(user["id"])


def test_invalid_jwt_token(client: TestClient):
    response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "test@example.com",
            "full_name": "Full Name Test",
            "password": "password",
        },
    )
    assert response.status_code == 200
    user = response.json()

    assert user["email"] == "test@example.com"
    response = client.post(
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        url="/api/v1/login/access-token",
        data={"username": user["email"], "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    # Modify the access token to make it invalid
    access_token = data["access_token"] + "invalid"

    # Verify that the JWT token is invalid
    with pytest.raises(jwt.exceptions.DecodeError):
        jwt.decode(access_token, algorithms=["HS256"])


def test_user_access_token(client: TestClient):
    response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "test@example.com",
            "full_name": "Full Name Test",
            "password": "password",
        },
    )
    assert response.status_code == 200

    user = response.json()
    response = client.post(
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        url="/api/v1/login/access-token",
        data={"username": user["email"], "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
