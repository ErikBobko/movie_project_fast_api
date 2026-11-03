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


def test_top_rated_empty_list(monkeypatch):
    received_limits = []
    def fake_get_top_rated(limit):
        received_limits.append(limit)
        return []
    monkeypatch.setattr(
        "routers.analytics.get_top_rated",
        fake_get_top_rated
    )
    response = client.get("/analytics/top-rated")


    assert response.status_code == 200
    assert response.json() == []
    assert received_limits == [10]


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_top_actors_returns_200(monkeypatch):
    def fake_top_actors():
        return [
            {"name":"Brad Pitt","movie_count" : 2},
            {"name":"Leonardo Di Caprio","movie_count" : 5}
        ]

    monkeypatch.setattr(
        "routers.analytics.get_top_actors_by_movie_count",
        fake_top_actors
    )

    response = client.get("/analytics/actors/top")

    assert response.status_code == 200
    assert response.json() == [
            {"name":"Brad Pitt","movie_count" : 2},
            {"name":"Leonardo Di Caprio","movie_count" : 5}
        ]



def test_top_actors_empty_list(monkeypatch):
    def fake_top_actors():
        return []
    monkeypatch.setattr(
        "routers.analytics.get_top_actors_by_movie_count",
        fake_top_actors
    )

    response = client.get("/analytics/actors/top")

    assert response.status_code == 200
    assert response.json() == []

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def test_highest_rated_actors_returns_200(monkeypatch):
    def fake_highest_actors():
        return [{"name":"Brad Pitt","rating" : 8.2},
                {"name":"Leonardo Di Caprio","rating" : 8.5}]


    monkeypatch.setattr(
        "routers.analytics.get_highest_rated_actors",
        fake_highest_actors
    )

    response = client.get("/analytics/actors/highest-rated")

    assert response.status_code == 200
    assert response.json() == [
        {"name": "Brad Pitt", "rating": 8.2},
        {"name": "Leonardo Di Caprio", "rating": 8.5}
    ]



def test_highest_rated_actors_empty_list(monkeypatch):
    def fake_highest_actors():
        return []

    monkeypatch.setattr(
        "routers.analytics.get_highest_rated_actors",
        fake_highest_actors
    )
    response = client.get("/analytics/actors/highest-rated")

    assert response.status_code == 200
    assert response.json() == []

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_get_most_popular_actors_returns_200(monkeypatch):
    def fake_most_popular_actors():

        return [
    {"name": "Brad Pitt", "movie_count": 8, "avg_popularity": 85.5},
    {"name": "Leonardo DiCaprio", "movie_count": 6, "avg_popularity": 78.2}
]

    monkeypatch.setattr(
        "routers.analytics.get_most_popular_actors",
        fake_most_popular_actors
    )

    response = client.get("/analytics/actors/popular")

    assert response.status_code == 200
    assert response.json() == [
    {"name": "Brad Pitt", "movie_count": 8, "avg_popularity": 85.5},
    {"name": "Leonardo DiCaprio", "movie_count": 6, "avg_popularity": 78.2}
]



def test_get_most_popular_actors_empty_list(monkeypatch):
    def fake_most_popular_actors():

        return []
    monkeypatch.setattr(
        "routers.analytics.get_most_popular_actors",
        fake_most_popular_actors
    )

    response = client.get("/analytics/actors/popular")
    assert response.status_code == 200
    assert response.json() == []

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def test_best_actors_returns_200(monkeypatch):
    def fake_best_actors():
        return [
            {"name": "Brad Pitt", "avg_rating": 8.0, "movie_count": 4,"actor_score": 12.88},
            {"name": "Leonardo DiCaprio", "avg_rating": 9.0, "movie_count": 10,"actor_score": 13.88},
            {"name": "Tom Cruise", "avg_rating": 7.0, "movie_count": 6,"actor_score": 14.88},
        ]
    monkeypatch.setattr(
            "routers.analytics.get_best_actors",
            fake_best_actors
        )
    response = client.get("/analytics/actors/best")

    assert response.status_code == 200
    assert response.json() == [
            {"name": "Brad Pitt", "avg_rating": 8.0, "movie_count": 4,"actor_score": 12.88},
            {"name": "Leonardo DiCaprio", "avg_rating": 9.0, "movie_count": 10,"actor_score": 13.88},
            {"name": "Tom Cruise", "avg_rating": 7.0, "movie_count": 6,"actor_score": 14.88},
        ]

def test_best_actors_empty_list(monkeypatch):
    def fake_best_actors():
        return []
    monkeypatch.setattr(
        "routers.analytics.get_best_actors",
        fake_best_actors
    )
    response = client.get("/analytics/actors/best")
    assert response.status_code == 200
    assert response.json() == []


