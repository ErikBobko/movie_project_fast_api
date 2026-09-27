from db import supabase


def fetch_movie_actor_ids(movie_id: int):
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


def fetch_movies_by_actor_ids(actor_ids):
    response = (
        supabase
        .table("movie_actors")
        .select("movie_id, actor_id")
        .in_("actor_id", list(actor_ids))
        .execute()
    )

    return response.data


def fetch_movies_by_ids(movie_ids):
    response = (
        supabase
        .table("movies")
        .select("*")
        .in_("id", movie_ids)
        .execute()
    )

    return response.data