from clients.tmdb_client import get_movie_cast,get_actor_details
from db import supabase


def _sync_cast_for_movie(movie):
    db_movie_id = movie["id"]
    tmdb_id = movie["tmdb_id"]

    actors_synced = 0
    relations_synced = 0

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

    
    supabase.table("movies").update(
        {"cast_synced": True}
    ).eq("id", db_movie_id).execute()

    return actors_synced, relations_synced


def sync_movie_casts(limit: int = 100, offset: int = 0):
    movies = (
        supabase
        .table("movies")
        .select("id, tmdb_id, title")
        .order("id")
        .range(offset, offset + limit - 1)
        .execute()
        .data
    )

    movies_synced = 0
    actors_synced = 0
    relations_synced = 0

    for movie in movies:
        actor_count, relation_count = _sync_cast_for_movie(movie)

        actors_synced += actor_count
        relations_synced += relation_count
        movies_synced += 1

    return {
        "movies_synced": movies_synced,
        "actors_processed": actors_synced,
        "relations_synced": relations_synced,
    }


def sync_missing_movie_casts(limit: int = 100):
    movies = (
        supabase
        .table("movies")
        .select("id, tmdb_id, title, cast_synced")
        .eq("cast_synced", False)
        .order("id")
        .limit(limit)
        .execute()
        .data
    )

    movies_synced = 0
    actors_synced = 0
    relations_synced = 0

    for movie in movies:
        actor_count, relation_count = _sync_cast_for_movie(movie)

        actors_synced += actor_count
        relations_synced += relation_count
        movies_synced += 1

    return {
        "movies_synced": movies_synced,
        "actors_processed": actors_synced,
        "relations_synced": relations_synced,
    }

def sync_actor_details(limit=1000):
    actors_response = (
        supabase
        .table("actors")
        .select("*")
        .limit(limit)
        .eq("details_synced", False)
        .execute()
    )

    actors = actors_response.data

    updated = 0

    for actor in actors:
        try:
            details = get_actor_details(
                actor["tmdb_actor_id"]
            )

            update_payload = {
                "details_synced": True,
                "birthday": details.get("birthday"),
                "place_of_birth": details.get("place_of_birth"),
                "biography": details.get("biography"),
                "popularity": details.get("popularity"),
            }

            (
                supabase
                .table("actors")
                .update(update_payload)
                .eq("id", actor["id"])
                .execute()
            )

            updated += 1

        except Exception as e:
            print(
                f"Failed actor {actor['name']}: {e}"
            )

    return {
        "updated": updated,
        "total": len(actors)
    }