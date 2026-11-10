
from uuid import UUID

import httpx
from sqlmodel import Session

from app.history import save_health_result
from app.monitoring import check_url


def test_history_initially_empty(client):
    response = client.post(
        "/services",
        json={
            "name": "Demo API",
            "health_url": "https://example.com/health",
        },
    )

    service_id = response.json()["id"]

    history = client.get(
        f"/services/{service_id}/checks"
    )

    assert history.status_code == 200
    assert history.json() == []


def test_save_and_retrieve_health_check(client, test_engine):
    response = client.post(
        "/services",
        json={
            "name": "Payment API",
            "health_url": "https://example.com/health",
        },
    )

    service_id = UUID(response.json()["id"])

    transport = httpx.MockTransport(
        lambda request: httpx.Response(503)
    )

    result = check_url(
        "https://example.com/health",
        transport=transport,
    )

    with Session(test_engine) as session:
        save_health_result(session, service_id, result)

    history = client.get(
        f"/services/{service_id}/checks"
    )

    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["status"] == "unhealthy"
    assert history.json()[0]["http_status"] == 503
    assert history.json()[0]["service_id"] == str(service_id)
    assert "checked_at" in history.json()[0]


def test_history_for_unknown_service(client):
    response = client.get(
        "/services/00000000-0000-4000-8000-000000000000/checks"
    )

    assert response.status_code == 404
