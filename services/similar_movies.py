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


def get_similar_movies(movie_id: int):
    movie = get_movie_by_id(movie_id)

    if not movie:
        return []

    actor_ids = get_movie_actor_ids(movie_id)

    return {
        "movie": movie["title"],
        "actor_count": len(actor_ids),
    }