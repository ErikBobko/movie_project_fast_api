
from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)

def test_get_similar_movies_success(monkeypatch):
    received_param = []
    def mock_get_similar_movies(movie_id):
        received_param.append(movie_id)
        fake_movies = [
            {"title": "Se7en", "rating": 8.6},
            {"title": "The Game", "rating": 7.7},
        ]
        return fake_movies

    monkeypatch.setattr(
        "routers.similar_movies.get_similar_movies",
        mock_get_similar_movies,
    )

    response = test_client.get("/movies/550/similar")

    assert response.status_code == 200
    assert response.json() == [{"title": "Se7en", "rating": 8.6},{"title": "The Game", "rating": 7.7}]
    assert received_param == [550]


def test_get_similar_movies_invalid_id(monkeypatch):
    called = []

    def mock_get_similar_movies(movie_id):
        called.append(True)


    monkeypatch.setattr(
        "routers.similar_movies.get_similar_movies",
        mock_get_similar_movies,
    )

    response = test_client.get("/movies/-5/similar")
    assert response.status_code == 422
    assert called == []




    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




def test_get_similar_movies_by_content_success(monkeypatch):
    received_param = []
    def mock_get_similar_movies(movie_id,limit):

        received_param.append((movie_id,limit))
        fake_movies = [
            {"title": "Se7en", "rating": 8.6},
        ]
        return fake_movies
    monkeypatch.setattr(
        "routers.similar_movies.get_similar_movies_by_content",
        mock_get_similar_movies,

    )
    response = test_client.get("/movies/550/similar/content?limit=5")

    assert response.status_code == 200
    assert response.json() == [{"title": "Se7en", "rating": 8.6}]
    assert received_param == [(550,5)]



def test_get_similar_movies_by_content_default_limit(monkeypatch):
    received_param = []
    def mock_get_similar_movies(movie_id,limit):
        received_param.append((movie_id,limit))
        return []

    monkeypatch.setattr(
        "routers.similar_movies.get_similar_movies_by_content",
        mock_get_similar_movies,
    )

    response = test_client.get("/movies/550/similar/content")
    assert response.status_code == 200
    assert received_param == [(550,10)]
    assert response.json() == []


def test_get_similar_movies_by_content_invalid_limit(monkeypatch):
    called = []
    def mock_get_similar_movies(movie_id,limit):
        called.append(True)

    monkeypatch.setattr(
        "routers.similar_movies.get_similar_movies_by_content",
        mock_get_similar_movies,
    )

    response = test_client.get("/movies/550/similar/content?limit=-5")

    assert response.status_code == 422
    assert called == []


def test_get_similar_movies_by_content_limit_too_high(monkeypatch):
    called = []

    def mock_get_similar_movies(movie_id, limit):
        called.append(True)

    monkeypatch.setattr(
        "routers.similar_movies.get_similar_movies_by_content",
        mock_get_similar_movies,
    )

    response = test_client.get("/movies/550/similar/content?limit=101")

    assert response.status_code == 422
    assert called == []

def test_get_similar_movies_by_content_invalid_id():
    response = test_client.get("/movies/-5/similar/content")
    assert response.status_code == 422


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



def test_get_hybrid_similar_movies_success(monkeypatch):
    received_param = []
    def mock_get_similar_movies(movie_id,limit):
        received_param.append((movie_id,limit))
        fake_movies = [
            {"title": "Se7en", "rating": 8.6},
        ]
        return fake_movies

    monkeypatch.setattr(
        "routers.similar_movies.get_hybrid_similar_movies",
        mock_get_similar_movies,
    )

    response = test_client.get("/movies/550/similar/hybrid?limit=5")

    assert response.status_code == 200
    assert response.json() == [{"title": "Se7en", "rating": 8.6}]
    assert received_param == [(550, 5)]


def test_get_hybrid_similar_movies_default_limit(monkeypatch):
    received_param = []
    def mock_get_similar_movies(movie_id,limit):
        received_param.append((movie_id,limit))
        return []
    monkeypatch.setattr(
        "routers.similar_movies.get_hybrid_similar_movies",
        mock_get_similar_movies,
    )
    response = test_client.get("/movies/550/similar/hybrid")
    assert response.status_code == 200
    assert received_param == [(550,10)]
    assert response.json() == []

def test_get_hybrid_similar_movies_invalid_id():
    response = test_client.get("/movies/-5/similar/hybrid")
    assert response.status_code == 422

def test_get_hybrid_similar_movies_invalid_limit():
    response = test_client.get("/movies/550/similar/hybrid?limit=-1")
    assert response.status_code == 422

def test_get_hybrid_similar_movies_limit_too_high():
    response = test_client.get("/movies/550/similar/hybrid?limit=101")
    assert response.status_code == 422