import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_services_initially_empty(client):
    response = client.get("/services")

    assert response.status_code == 200
    assert response.json() == []


def test_create_service(client):
    response = client.post(
        "/services",
        json={
            "name": "Demo API",
            "health_url": "https://example.com/health",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Demo API"
    assert "id" in response.json()


def test_service_appears_in_list(client):
    client.post(
        "/services",
        json={
            "name": "Payment API",
            "health_url": "https://example.com/health",
        },
    )

    response = client.get("/services")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Payment API"


def test_invalid_url_rejected(client):
    response = client.post(
        "/services",
        json={
            "name": "Invalid API",
            "health_url": "not-a-valid-url",
        },
    )

    assert response.status_code == 422
