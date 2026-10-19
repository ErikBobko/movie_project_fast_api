from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_movies_invalid_limit():
    response = client.get("/movies?limit=0")
    assert response.status_code == 422


def test_get_movies_invalid_offset():
    response = client.get("/movies?offset=-1")
    assert response.status_code == 422


def test_get_movies_too_high_limit():
    response = client.get("/movies?limit=101")
    assert response.status_code == 422

def test_get_movies_returns_200(monkeypatch):
    received_params = []
    def fake_get_movies(limit, offset):
        received_params.append((limit,offset))
        return [
            {"title":"Titanic","rating":8.2},
            {"title":"Pulp Fiction","rating":9.3},
        ]

    monkeypatch.setattr(
        "routers.movies.get_all_movies",
        fake_get_movies
    )

    response = client.get("/movies?limit=5&offset=10")

    assert response.status_code == 200
    assert response.json() == [
            {"title":"Titanic","rating":8.2},
            {"title":"Pulp Fiction","rating":9.3},
        ]
    assert received_params == [(5,10)]



def test_get_movies_empty_list(monkeypatch):
    received_params = []
    def fake_get_movies(limit, offset):
        received_params.append((limit,offset))
        return []
    monkeypatch.setattr(
        "routers.movies.get_all_movies",
        fake_get_movies
    )

    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json() == []
    assert received_params == [(100,0)]



