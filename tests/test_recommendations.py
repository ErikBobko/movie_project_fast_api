from fastapi.testclient import TestClient

import routers.recommendations
from main import app

test_client = TestClient(app)


def test_get_recommendations_success(monkeypatch):
    received_params = {}
    def mock_get_recommendations(**kwargs):
        received_params["genre"] = kwargs["genre"]
        received_params["limit"] = kwargs["limit"]
        received_params["min_rating"] = kwargs["min_rating"]

        fake_movies = [
            {"title": "Inception", "rating": 8.8},
            {"title": "The Dark Knight", "rating": 9.0},
        ]

        return fake_movies
    monkeypatch.setattr(
        "routers.recommendations.get_recommendations"
        , mock_get_recommendations
    )

    response = test_client.get("/recommendations?genre=Action&min_rating=7.5&limit=5")

    assert response.status_code == 200
    assert response.json() == [{"title": "Inception", "rating": 8.8}, {"title": "The Dark Knight", "rating": 9.0}]
    assert received_params["genre"] == "Action"
    assert received_params["limit"] == 5
    assert received_params["min_rating"] == 7.5




def test_get_recommendations_default_params(monkeypatch):
    received_params = {}
    def mock_get_recommendations(**kwargs):
        received_params["genre"] = kwargs["genre"]
        received_params["limit"] = kwargs["limit"]
        received_params["min_rating"] = kwargs["min_rating"]
        received_params["min_vote_count"] = kwargs["min_vote_count"]
        return []

    monkeypatch.setattr(
        "routers.recommendations.get_recommendations"
        , mock_get_recommendations
    )

    response = test_client.get("/recommendations")


    assert response.status_code == 200
    assert response.json() == []
    assert received_params["genre"] is None
    assert received_params["limit"] == 10
    assert received_params["min_rating"] == 0
    assert received_params["min_vote_count"] == 100


def test_get_recommendations_invalid_limit(monkeypatch):
    called = []
    def mock_get_recommendations(**kwargs):
        called.append(True)

    monkeypatch.setattr(
        "routers.recommendations.get_recommendations"
        , mock_get_recommendations
    )

    response = test_client.get("/recommendations?limit=abc")
    assert response.status_code == 422
    assert called == []

def test_get_recommendations_empty_result(monkeypatch):
    fake_movies = []
    def mock_get_recommendations(**kwargs):

        return fake_movies

    monkeypatch.setattr(
        "routers.recommendations.get_recommendations"
        , mock_get_recommendations
    )

    response = test_client.get("/recommendations")

    assert response.json() == []
    assert response.status_code == 200







