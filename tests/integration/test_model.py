from fastapi.testclient import TestClient
from models.models import ModelType


def test_get_models_unauthorized(client: TestClient):
    response = client.get("/api/v1/models")
    assert response.status_code == 401


def test_get_models(client: TestClient, user_header: dict):
    response = client.get("/api/v1/models", headers=user_header)
    response_data = response.json()

    assert response_data["count"] == 0
    assert response_data["data"] == []


def test_create_model_success(client: TestClient, user_header: dict):
    model_name = "Model 1"
    model_description = "Model 1 description"
    model_type = ModelType.image_classification.value

    response = client.post(
        "/api/v1/models",
        headers=user_header,
        json={
            "name": model_name,
            "description": model_description,
            "model_type": model_type,
        },
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["name"] == model_name
    assert response_data["description"] == model_description
    assert response_data["model_type"] == model_type


def test_create_model_with_wrong_type_raises(client: TestClient, user_header: dict):
    model_name = "Model 1"
    model_description = "Model 1 description"
    model_type = "wrong_type"

    response = client.post(
        "/api/v1/models",
        headers=user_header,
        json={
            "name": model_name,
            "description": model_description,
            "model_type": model_type,
        },
    )

    assert response.status_code == 422


def test_create_model_is_retrieved_from_list(client: TestClient, user_header: dict):
    model_name = "Model 1"
    model_description = "Model 1 description"
    model_type = ModelType.image_classification.value

    response = client.post(
        "/api/v1/models",
        headers=user_header,
        json={
            "name": model_name,
            "description": model_description,
            "model_type": model_type,
        },
    )

    response = client.get("/api/v1/models", headers=user_header)
    response_data = response.json()
    assert response_data["count"] == 1
    assert response_data["data"][0]["name"] == model_name
    assert response_data["data"][0]["description"] == model_description
    assert response_data["data"][0]["model_type"] == model_type


def test_update_model_success(client: TestClient, user_header: dict):
    model_name = "Model 1"
    model_description = "Model 1 description"
    model_type = ModelType.image_classification.value

    response = client.post(
        "/api/v1/models",
        headers=user_header,
        json={
            "name": model_name,
            "description": model_description,
            "model_type": model_type,
        },
    )
    response_data = response.json()

    new_description = "New description"
    response = client.put(
        f"/api/v1/models/{response_data['id']}",
        headers=user_header,
        json={
            "name": model_name,
            "description": new_description,
            "model_type": model_type,
        },
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["description"] == new_description
