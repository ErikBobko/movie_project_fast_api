from clients.tmdb_client import get_movie_cast
from db import supabase


def sync_movie_casts(limit: int | None = None):
    query = (
        supabase
        .table("movies")
        .select("id, tmdb_id, title")
        .order("id")
    )

    if limit:
        query = query.limit(limit)

    movies = query.execute().data

    movies_synced = 0
    actors_synced = 0
    relations_synced = 0

    for movie in movies:
        db_movie_id = movie["id"]
        tmdb_id = movie["tmdb_id"]

        cast = get_movie_cast(tmdb_id, limit=10)

        for actor in cast:
            actor_payload = {
                "tmdb_actor_id": actor["id"],
                "name": actor["name"],
                "profile_path": actor["profile_path"],
            }

            actor_response = (
                supabase
                .table("actors")
                .upsert(actor_payload, on_conflict="tmdb_actor_id")
                .execute()
            )

            if not actor_response.data:
                continue

            saved_actor = actor_response.data[0]

            relation_payload = {
                "movie_id": db_movie_id,
                "actor_id": saved_actor["id"],
                "character": actor["character"],
                "cast_order": actor["order"],
            }

            supabase.table("movie_actors").upsert(
                relation_payload,
                on_conflict="movie_id,actor_id"
            ).execute()

            actors_synced += 1
            relations_synced += 1

        movies_synced += 1

    return {
        "movies_synced": movies_synced,
        "actors_processed": actors_synced,
        "relations_synced": relations_synced,
    }