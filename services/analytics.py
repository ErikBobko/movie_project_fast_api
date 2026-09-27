
from repositories.analytics import (
    fetch_top_rated,
    fetch_movies,
    fetch_movies_count,
)


def get_top_rated(limit: int = 10):
    return fetch_top_rated(limit)


def get_movies():
    return fetch_movies()

def get_movies_count():
    return fetch_movies_count()


def get_kpis():
    movies = get_movies()

    total_movies = get_movies_count()

    avg_rating = (
        sum(movie["rating"] for movie in movies)
        / len(movies)
        if movies
        else 0
    )

    return {
        "total_movies": total_movies,
        "avg_rating": avg_rating
    }



