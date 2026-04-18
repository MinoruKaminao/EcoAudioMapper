from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.models.observation import Observation
from app.db.session import get_session_factory


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "development",
    }


def test_list_observations_returns_empty_collection(client: TestClient) -> None:
    response = client.get("/api/v1/observations")

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "limit": 20,
        "offset": 0,
    }


def test_list_observations_returns_seeded_rows(client: TestClient) -> None:
    session = get_session_factory()()
    try:
        session.add(
            Observation(
                user_id=uuid4(),
                media_file_id=uuid4(),
                location_id=uuid4(),
                observation_datetime_id=uuid4(),
                source_type="imported",
                visibility_level="public",
                status="uploaded",
            )
        )
        session.commit()
    finally:
        session.close()

    response = client.get("/api/v1/observations")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["limit"] == 20
    assert body["offset"] == 0
    assert len(body["items"]) == 1
    assert body["items"][0]["status"] == "uploaded"
    assert body["items"][0]["visibility_level"] == "public"
    assert body["items"][0]["recorded_at_utc"] is None
