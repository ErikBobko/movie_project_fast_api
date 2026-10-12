from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_top_rated_invalid_limit():
    response = client.get("/analytics/top-rated?limit=0")

    assert response.status_code == 422

def test_top_rated_limit_too_high():
    response = client.get("/analytics/top-rated?limit=150")

    assert response.status_code == 422

def test_top_rated_success(monkeypatch):
    received_limits = []

    def fake_get_top_rated(limit):
        received_limits.append(limit)
        return [
            {"title": "Interstellar", "rating": 8.7},
            {"title": "Inception", "rating": 8.8}
        ]

    monkeypatch.setattr(
        "routers.analytics.get_top_rated",
        fake_get_top_rated
    )

    response = client.get("/analytics/top-rated?limit=5")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert received_limits == [5]

