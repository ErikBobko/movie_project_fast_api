from db import supabase


def fetch_actors_by_name(actor_name: str):
    response = (
        supabase
        .table("actors")
        .select("id, name")
        .ilike("name", f"%{actor_name}%")
        .limit(10)
        .execute()
    )

    return response.data or []

def fetch_movie_ids_by_actor_ids(actor_ids: list[int]):
    response = (
        supabase
        .table("movie_actors")
        .select("movie_id")
        .in_("actor_id", actor_ids)
        .execute()
    )

    return response.data or []

def fetch_actor_relations_by_movie_ids(movie_ids: list[int]):
    response = (
        supabase
        .table("movie_actors")
        .select("movie_id, actor_id")
        .in_("movie_id", movie_ids)
        .execute()
    )

    return response.data or []

def fetch_actors_by_ids(actor_ids: list[int]):
    response = (
        supabase
        .table("actors")
        .select("id, name")
        .in_("id", actor_ids)
        .execute()
    )

    return response.data or []


def fetch_recommendation_candidates(
    min_rating: float,
    min_vote_count: int,
    year: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    movie_ids: list[int] | None = None,
    limit: int = 1000,
):
    query = (
        supabase
        .table("movies")
        .select("*")
        .gte("rating", min_rating)
        .gte("vote_count", min_vote_count)
        .not_.is_("rating", "null")
    )

    if year is not None:
        query = query.eq("year", year)
    else:
        if year_from is not None:
            query = query.gte("year", year_from)

        if year_to is not None:
            query = query.lte("year", year_to)

    if movie_ids is not None:
        query = query.in_("id", movie_ids)

    response = query.limit(limit).execute()

    return response.data or []