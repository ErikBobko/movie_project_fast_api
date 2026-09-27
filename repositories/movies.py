from db import supabase


def fetch_all_movies(limit: int, offset: int):
    response = (
        supabase
        .table("movies")
        .select("*")
        .range(
            offset,
            offset + limit - 1,
        )
        .execute()
    )

    return response.data or []

def fetch_movie_by_tmdb_id(tmdb_id: int):
    response = (
        supabase
        .table("movies")
        .select("*")
        .eq("tmdb_id", tmdb_id)
        .maybe_single()
        .execute()
    )

    return response.data

def insert_movie(movie_data: dict):
    response = (
        supabase
        .table("movies")
        .insert(movie_data)
        .execute()
    )

    return response.data

def fetch_movie_by_id(movie_id: int):
    response = (
        supabase
        .table("movies")
        .select("*")
        .eq("id", movie_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]