from db import supabase


def get_movie_by_id(movie_id: int):
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