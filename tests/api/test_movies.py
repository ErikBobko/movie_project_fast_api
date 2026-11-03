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


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def test_movie_by_tmdb_id_invalid_id():

    response = client.get("/movies/by-tmdb-id/-5")
    assert response.status_code == 422

def test_movie_by_tmdb_id_success(monkeypatch):
    received_params = []
    def fake_get_movie_by_tmdb_id(tmdb_id):
        received_params.append((tmdb_id))

        return {
            "tmdb_id": 550,
            "title": "Fight Club",
            "rating": 8.4
        }

    monkeypatch.setattr(
        "routers.movies.get_movie_by_tmdb_id",
        fake_get_movie_by_tmdb_id
    )

    response = client.get("/movies/by-tmdb-id/550")

    assert response.status_code == 200
    assert response.json() == {
            "tmdb_id": 550,
            "title": "Fight Club",
            "rating": 8.4
        }
    assert received_params == [550]

def test_movie_by_tmdb_id_not_found(monkeypatch):
    received_params = []
    def fake_get_movie_by_tmdb_id(tmdb_id):
        received_params.append((tmdb_id))
        return None

    monkeypatch.setattr(
        "routers.movies.get_movie_by_tmdb_id",
        fake_get_movie_by_tmdb_id
    )

    response = client.get("/movies/by-tmdb-id/999999")
    assert response.status_code == 404
    assert received_params == [999999]
    assert response.json() == {"detail": "Movie not found"}


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def test_movie_by_id_success(monkeypatch):
    received_params = []
    def fake_get_movie_by_id(tmdb_id):
        received_params.append((tmdb_id))
        return {"id": 10, "title": "Inception"}
    monkeypatch.setattr(
        "routers.movies.get_movie_by_id",
        fake_get_movie_by_id
    )

    response = client.get("/movies/by-id/10")

    assert response.status_code == 200
    assert response.json() == {"id": 10, "title": "Inception"}
    assert received_params == [10]

def test_movie_by_id_not_found(monkeypatch):
    received_params = []
    def fake_get_movie_by_id(tmdb_id):
        received_params.append((tmdb_id))
        return None
    monkeypatch.setattr(
        "routers.movies.get_movie_by_id",
        fake_get_movie_by_id
    )

    response = client.get("/movies/by-id/999999")

    assert response.status_code == 404
    assert received_params == [999999]
    assert response.json() == {"detail": "Movie not found"}



def test_movie_by_id_invalid():

    response = client.get("/movies/by-id/0")
    assert response.status_code == 422


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_get_movie_cast_success(monkeypatch):
    received_params = []
    def fake_get_movie_cast(tmdb_id):
        received_params.append((tmdb_id))
        return [{"name": "Brad Pitt"}]


    monkeypatch.setattr(
        "routers.movies.get_movie_cast",
        fake_get_movie_cast
    )
    response = client.get("/movies/55/cast")


    assert response.status_code == 200
    assert response.json() == [{"name": "Brad Pitt"}]
    assert received_params == [55]


def test_get_movie_cast_invalid_id():

    response = client.get("/movies/-5/cast")
    assert response.status_code == 422

def test_get_movie_cast_empty(monkeypatch):
    def fake_get_movie_cast(tmdb_id):
        return []
    monkeypatch.setattr(
        "routers.movies.get_movie_cast",
        fake_get_movie_cast
    )

    response = client.get("/movies/55/cast")
    assert response.status_code == 200
    assert response.json() == []

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_get_movie_crew_success(monkeypatch):
    received_params = []
    def fake_get_movie_crew(tmdb_id):
        received_params.append((tmdb_id))

        return {"director": "David Fincher"}

    monkeypatch.setattr(
        "routers.movies.get_movie_crew_summary",
        fake_get_movie_crew
    )

    response = client.get("/movies/550/crew")


    assert response.status_code == 200
    assert response.json() == {"director": "David Fincher"}
    assert received_params == [550]



def test_get_movie_crew_invalid_id():

    response = client.get("/movies/-5/crew")
    assert response.status_code == 422


def test_get_movie_crew_empty(monkeypatch):
    def fake_get_movie_crew(tmdb_id):
        return None

    monkeypatch.setattr(
        "routers.movies.get_movie_crew_summary",
        fake_get_movie_crew
    )

    response = client.get("/movies/55/crew")

    assert response.status_code == 200
    assert response.json()  is None

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_create_movie_success(monkeypatch):
    movie_data = {
        "title": "Fight Club",
        "tmdb_id": 550,
        "rating": 8.8
    }
    def fake_create_movie(movie):
        return movie_data
    monkeypatch.setattr(
        "routers.movies.create_movie",
        fake_create_movie

    )

    response = client.post("/movies", json=movie_data)
    assert response.status_code == 201
    assert response.json() == {"title": "Fight Club",
        "tmdb_id": 550,
        "rating": 8.8}



def test_create_movie_missing_title():
    movie_data = {
        "tmdb_id": 550,
        "rating": 8.8
    }

    response = client.post("/movies", json=movie_data)
    assert response.status_code == 422



def test_create_movie_invalid_rating():
    movie_data = {
        "title": "Fight Club",
        "rating":"abc",
    }

    response = client.post("/movies", json=movie_data)

    assert response.status_code == 422



def test_create_movie_successful(monkeypatch):
    movie_data = {
        "title": "Fight Club",
    }
    response = client.post("/movies", json=movie_data)

    assert response.status_code == 201


