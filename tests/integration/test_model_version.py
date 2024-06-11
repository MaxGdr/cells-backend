from fastapi.testclient import TestClient
from models.models import ModelType
import pytest


@pytest.fixture()
def created_model(client: TestClient, user_header: dict) -> dict:
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
    return response.json()


def test_get_model_versions_unauthorized(client: TestClient):
    response = client.get("/api/v1/models/1/modelversions")
    assert response.status_code == 401


def test_get_model_versions(client: TestClient, user_header: dict, created_model: dict):
    response = client.get(
        f"/api/v1/models/{created_model['id']}/modelversions", headers=user_header
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["count"] == 0
    assert response_data["data"] == []


def test_create_model_version_success(
    client: TestClient, user_header: dict, created_model: dict
):
    expected_model_version_number = 1
    endpoint_id = "2134125"
    description = "Model version 1 description"

    response = client.post(
        f"/api/v1/models/{created_model['id']}/modelversions",
        headers=user_header,
        json={"endpoint_id": endpoint_id, "description": description},
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["number"] == expected_model_version_number
    assert response_data["endpoint_id"] == endpoint_id
    assert response_data["description"] == description


def test_create_successive_version_increment_num(
    client: TestClient, user_header: dict, created_model: dict
):
    expected_model_version_number = 3
    endpoint_id = "2134125"

    for i in range(1, 4):
        response = client.post(
            f"/api/v1/models/{created_model['id']}/modelversions",
            headers=user_header,
            json={
                "endpoint_id": f"{endpoint_id}{i}",
                "description": f"Model version {i} description",
            },
        )
        assert response.status_code == 200
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["number"] == expected_model_version_number
    assert response_data["endpoint_id"] == f"{endpoint_id}{i}"
    assert (
        response_data["description"]
        == f"Model version {expected_model_version_number} description"
    )


def test_create_model_version_with_duplicates_endpoint_raises(
    client: TestClient, user_header: dict, created_model: dict
):
    endpoint_id = "2134125"

    response_a = client.post(
        f"/api/v1/models/{created_model['id']}/modelversions",
        headers=user_header,
        json={"endpoint_id": endpoint_id, "description": "Model version description"},
    )
    assert response_a.status_code == 200

    response_b = client.post(
        f"/api/v1/models/{created_model['id']}/modelversions",
        headers=user_header,
        json={"endpoint_id": endpoint_id, "description": "Model version description"},
    )
    assert response_b.status_code == 400


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
