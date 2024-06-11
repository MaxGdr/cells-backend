from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    response = client.get("/api/v1/users")

    assert response.status_code == 200
    assert response.json() == {"data": [], "count": 0}

    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "full_name": "Full Name Test",
            "password": "password",
        },
    )
    assert response.status_code == 200

    response = client.get("/api/v1/users")
    data = response.json()
    assert len(data["data"]) == 1
    assert data["count"] == 1

    assert data["data"][0]["email"] == "test@example.com"
    assert data["data"][0]["full_name"] == "Full Name Test"
    assert not data["data"][0]["password"] == "password"
