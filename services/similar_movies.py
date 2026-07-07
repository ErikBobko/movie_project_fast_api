from db import supabase
from services.movies import get_movie_by_id


def get_movie_actor_ids(movie_id: int):
    response = (
        supabase
        .table("movie_actors")
        .select("actor_id")
        .eq("movie_id", movie_id)
        .execute()
    )

    return {
        row["actor_id"]
        for row in response.data
    }


def get_movies_by_actor_ids(actor_ids):
    response = (
        supabase
        .table("movie_actors")
        .select("movie_id, actor_id")
        .in_("actor_id", list(actor_ids))
        .execute()
    )

    return response.data


def get_similar_movies(movie_id: int):
    movie = get_movie_by_id(movie_id)

    if not movie:
        return []

    actor_ids = get_movie_actor_ids(movie_id)

    if not actor_ids:
        return []

    movie_actor_rows = get_movies_by_actor_ids(actor_ids)

    movie_scores = {}

    for row in movie_actor_rows:
        similar_movie_id = row["movie_id"]

        if similar_movie_id == movie_id:
            continue

        movie_scores[similar_movie_id] = (
            movie_scores.get(similar_movie_id, 0) + 1
        )

    sorted_movie_ids = sorted(
        movie_scores,
        key=movie_scores.get,
        reverse=True
    )[:10]

    movies = get_movies_by_ids(sorted_movie_ids)

    for movie_data in movies:
        movie_data["shared_actor_count"] = movie_scores.get(
            movie_data["id"],
            0
        )

    movies = sorted(
        movies,
        key=lambda movie: movie["shared_actor_count"],
        reverse=True
    )

    return movies

def get_movies_by_ids(movie_ids):
    response = (
        supabase
        .table("movies")
        .select("*")
        .in_("id", movie_ids)
        .execute()
    )

    return response.data