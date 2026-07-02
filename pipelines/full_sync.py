from pipelines.ingestion import sync_popular_movies
from pipelines.cast_sync import sync_missing_movie_casts, sync_actor_details


def sync_full_database(
    pages: int = 50,
    cast_limit: int = 1000,
    actor_details_limit: int = 1000,
):
    movies = sync_popular_movies(pages=pages)

    cast_result = sync_missing_movie_casts(limit=cast_limit)

    actor_details_result = sync_actor_details(limit=actor_details_limit)

    return {
        "movies_synced": len(movies),
        "cast_sync": cast_result,
        "actor_details_sync": actor_details_result,
    }