from db import supabase


def fetch_top_rated(limit: int = 10):
    response = (
        supabase
        .table("movies")
        .select("*")
        .gte("vote_count", 10000)
        .order("rating", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data

def fetch_movies():
    response = (
        supabase
        .table("movies")
        .select("*")
        .range(0, 11000)
        .execute()
    )

    return response.data


def fetch_movies_count():
    response = (
        supabase
        .table("movies")
        .select("*", count="exact")
        .execute()
    )

    return response.count