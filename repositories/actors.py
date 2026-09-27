from db import supabase


def fetch_actor_by_tmdb_id(tmdb_actor_id: int):
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


def fetch_movie_ids_by_actor_id(actor_id: int):
    response = (
        supabase
        .table("movie_actors")
        .select("movie_id")
        .eq("actor_id", actor_id)
        .execute()
    )

    return [relation["movie_id"] for relation in response.data]


def fetch_movies_by_ids(movie_ids: list[int]):
    response = (
        supabase
        .table("movies")
        .select("*")
        .in_("id", movie_ids)
        .execute()
    )

    return response.data



def fetch_all_actors(
    limit: int = 50,
    offset: int = 0,
    search: str | None = None
):
    query = (
        supabase
        .table("actors")
        .select("*")
        .order("name")
    )

    if search:
        query = query.ilike("name", f"%{search}%")

    response = (
        query
        .range(offset, offset + limit - 1)
        .execute()
    )

    return response.data