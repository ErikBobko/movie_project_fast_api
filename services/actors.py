from db import supabase


def get_actor_by_tmdb_id(tmdb_actor_id: int):
    response = (
        supabase
        .table("actors")
        .select("*")
        .eq("tmdb_actor_id", tmdb_actor_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def get_actor_movies_by_tmdb_id(tmdb_actor_id: int):
    actor = get_actor_by_tmdb_id(tmdb_actor_id)

    if not actor:
        return []

    relations_response = (
        supabase
        .table("movie_actors")
        .select("movie_id")
        .eq("actor_id", actor["id"])
        .execute()
    )

    movie_ids = [r["movie_id"] for r in relations_response.data]

    if not movie_ids:
        return []

    movies_response = (
        supabase
        .table("movies")
        .select("*")
        .in_("id", movie_ids)
        .execute()
    )

    return movies_response.data

def get_all_actors(limit: int = 100):
    response = (
        supabase
        .table("actors")
        .select("*")
        .order("name")
        .limit(limit)
        .execute()
    )

    return response.data