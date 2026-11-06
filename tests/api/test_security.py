from fastapi.testclient import TestClient
from main import app


client = TestClient(app)



def test_missing_api_key(monkeypatch):
    monkeypatch.setenv("SYNC_API_KEY", "test-secret")

    response = client.post(
        "/ai/recommendations",
        json={"prompt": "Recommend a horror movie"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_invalid_api_key(monkeypatch):
    monkeypatch.setenv("SYNC_API_KEY", "test-secret")

    response = client.post(
        "/ai/recommendations",
        json={"prompt": "Recommend a horror movie"},
        headers={"X-API-Key": "wrong-secret"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_valid_api_key(monkeypatch):
    monkeypatch.setenv("SYNC_API_KEY", "test-secret")

    def fake_recommendations(prompt):
        return {"recommendations": []}

    monkeypatch.setattr(
        "routers.ai.get_ai_recommendations",
        fake_recommendations
    )

    response = client.post(
        "/ai/recommendations",
        json={"prompt": "Recommend a horror movie"},
        headers={"X-API-Key": "test-secret"}
    )

    assert response.status_code == 200
    assert response.json() == {"recommendations": []}


def test_missing_api_key_configuration(monkeypatch):
    monkeypatch.delenv("SYNC_API_KEY", raising=False)

    response = client.post(
        "/ai/recommendations",
        json={"prompt": "Recommend a horror movie"},
        headers={"X-API-Key": "test-secret"}
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "Sync API is not configured"