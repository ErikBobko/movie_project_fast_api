from services.actor_analytics import get_best_actors


def test_best_actors_score_calculation(monkeypatch):
    def fake_fetch_actors_for_best_score():
        return [
    {
        "name": "Brad Pitt",
        "avg_rating": 8.0,
        "movie_count": 4
    }
]

    monkeypatch.setattr(
        "services.actor_analytics.fetch_actors_for_best_score",
        fake_fetch_actors_for_best_score
    )

    result = get_best_actors()

    assert result[0]["name"] == "Brad Pitt"
    assert result[0]["avg_rating"] == 8.0
    assert result[0]["movie_count"] == 4
    assert result[0]["actor_score"] == 12.88


def test_best_actors_sorting(monkeypatch):
    def fake_fetch_actors_for_best_score():
        return [
    {"name": "Brad Pitt", "avg_rating": 8.0, "movie_count": 4},
    {"name": "Leonardo DiCaprio", "avg_rating": 9.0, "movie_count": 10},
    {"name": "Tom Cruise", "avg_rating": 7.0, "movie_count": 6}
]
    monkeypatch.setattr(
        "services.actor_analytics.fetch_actors_for_best_score",
        fake_fetch_actors_for_best_score
    )
    result = get_best_actors()

    assert result == sorted(result, key=lambda actor: actor["actor_score"],reverse=True)

    assert [actor["name"] for actor in result] == [
        "Leonardo DiCaprio",
        "Tom Cruise",
        "Brad Pitt"
    ]

def test_best_actors_top_5(monkeypatch):
    def fake_fetch_actors_for_best_score():
        return [
    {"name": "Brad Pitt", "avg_rating": 8.0, "movie_count": 4},
    {"name": "Leonardo DiCaprio", "avg_rating": 9.0, "movie_count": 10},
    {"name": "Tom Cruise", "avg_rating": 7.0, "movie_count": 6},
    {"name": "Angelina Jolie", "avg_rating": 7.3, "movie_count": 6},
    {"name": "Tom Hanks", "avg_rating": 6.3, "movie_count": 5},
    {"name": "Bradley Cooper", "avg_rating": 7.8, "movie_count": 8},

]
    monkeypatch.setattr(
        "services.actor_analytics.fetch_actors_for_best_score",
        fake_fetch_actors_for_best_score
    )

    result = get_best_actors()

    assert len(result) == 5
    assert [actor["name"] for actor in result] == [
        "Leonardo DiCaprio",
        "Bradley Cooper",
       "Angelina Jolie",
        "Tom Cruise",
        "Brad Pitt"
    ]

def test_best_actors_empty_list(monkeypatch):
    def fake_fetch_actors_for_best_score():
        return []
    monkeypatch.setattr(
        "services.actor_analytics.fetch_actors_for_best_score",
        fake_fetch_actors_for_best_score
    )

    result = get_best_actors()

    assert result == []



