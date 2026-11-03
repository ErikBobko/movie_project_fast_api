from fastapi.testclient import TestClient

import pytest
from main import app


client = TestClient(app)

def test_sync_casts_success(monkeypatch):
    received_param = []
    def mock_sync_cast(**kwargs):
        received_param.append(kwargs)
        return {"synced": 5}

    monkeypatch.setattr(
        "routers.sync.sync_movie_casts",
        mock_sync_cast,
    )

    response = client.post("/sync/casts?limit=5&offset=10")

    assert response.status_code == 200
    assert response.json() == {"synced": 5}
    assert received_param == [{"limit": 5, "offset": 10}]


def test_sync_casts_default_params(monkeypatch):
    received_param = []
    def mock_sync_cast(**kwargs):
        received_param.append(kwargs)
        return {"synced": 0}

    monkeypatch.setattr(
        "routers.sync.sync_movie_casts",
        mock_sync_cast,
    )
    response = client.post("/sync/casts")

    assert response.status_code == 200
    assert response.json() == {"synced": 0}
    assert received_param == [{"limit": 100, "offset": 0}]


@pytest.mark.parametrize(
     "limit, offset", [
        (-5, 0),
        (101, 0),
        (5, -20),
    ], )
def test_sync_casts_invalid_params(limit, offset):
    response = client.post(f"/sync/casts?limit={limit}&offset={offset}")
    assert response.status_code == 422


    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



def test_sync_missing_casts_success(monkeypatch):
    received_param = []
    def mock_sync_missing_casts(limit):
        received_param.append(limit)
        return{
            "movies_synced": 0,
            "actors_processed": 0,
            "relations_synced": 0,
        }

    monkeypatch.setattr(
        "routers.sync.sync_missing_movie_casts",
        mock_sync_missing_casts,
    )

    response = client.post("/sync/casts/missing?limit=100")

    assert response.status_code == 200
    assert response.json() == {"movies_synced": 0,"actors_processed": 0,"relations_synced": 0}
    assert received_param == [100]


def test_sync_missing_casts_default_params(monkeypatch):
    received_param = []
    def mock_sync_missing_casts(limit):
        received_param.append(limit)

    monkeypatch.setattr(
        "routers.sync.sync_missing_movie_casts",
        mock_sync_missing_casts,

    )

    response = client.post("/sync/casts/missing")

    assert response.status_code == 200
    assert received_param == [100]


@pytest.mark.parametrize("limit",[ -1, 0, 1001])

def test_sync_missing_casts_invalid_params(limit):
    response = client.post(f"/sync/casts/missing?limit={limit}")
    assert response.status_code == 422


    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_sync_actors_details_success(monkeypatch):
    received_param = []
    def mock_sync_actors_details(limit):

        received_param.append(limit)

        fake_sync_actors_details = {"updated": 5,"total": 5}
        return fake_sync_actors_details
    monkeypatch.setattr(
        "routers.sync.sync_actor_details",
        mock_sync_actors_details,
    )

    response = client.post("/sync/actors/details?limit=100")

    assert response.status_code == 200
    assert response.json() == {"updated": 5, "total": 5}
    assert received_param == [100]



def test_sync_actors_details_default_params(monkeypatch):
    received_param = []
    def mock_sync_actors_details(limit):
        received_param.append(limit)

    monkeypatch.setattr(
        "routers.sync.sync_actor_details",
     mock_sync_actors_details,)
    response = client.post("/sync/actors/details")
    assert response.status_code == 200
    assert received_param == [100]


@pytest.mark.parametrize("limit",[ -1, 0, 1001])
def test_sync_actors_details_invalid_params(limit):
    response = client.post(f"/sync/actors/details?limit={limit}")
    assert response.status_code == 422

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def test_sync_popular_success(monkeypatch):
    received_param = []
    def mock_sync_popular(pages):
        received_param.append(pages)

        fake_sync_popular = [
            {"tmdb_id": 550, "title": "Fight Club"},
            {"tmdb_id": 27205, "title": "Inception"}
        ]
        return fake_sync_popular

    monkeypatch.setattr(
        "routers.sync.sync_popular_movies",
        mock_sync_popular,
    )
    response = client.post("/sync/popular?pages=5")


    assert response.status_code == 200
    assert response.json() == [
            {"tmdb_id": 550, "title": "Fight Club"},
            {"tmdb_id": 27205, "title": "Inception"}
        ]
    assert received_param == [5]

def test_sync_popular_default_params(monkeypatch):
    received_param = []
    def mock_sync_popular(pages):
        received_param.append(pages)

    monkeypatch.setattr(
        "routers.sync.sync_popular_movies",
        mock_sync_popular,
    )
    response = client.post("/sync/popular")

    assert response.status_code == 200
    assert received_param == [1]


@pytest.mark.parametrize("pages",[ -1, 0, 11])
def test_sync_popular_invalid_params(pages):
    response = client.post(f"/sync/popular?pages={pages}")
    assert response.status_code == 422


    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

