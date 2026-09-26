from fastapi import APIRouter

from pipelines.ingestion import sync_popular_movies
from pipelines.full_sync import sync_full_database
from pipelines.cast_sync import (
    sync_movie_casts,
    sync_missing_movie_casts,
    sync_actor_details,
)

router = APIRouter(prefix="/sync",tags=["Sync"])


@router.post("/casts")
def sync_casts(limit: int = 100, offset: int = 0):
    return sync_movie_casts(limit=limit, offset=offset)

@router.post("/casts/missing")
def sync_missing_casts(limit: int = 100):
    return sync_missing_movie_casts(limit)

@router.post("/actors/details")
def sync_actors_details(limit: int = 100):
    return sync_actor_details(limit)

@router.post("/popular")
def sync_movies(pages: int = 1):
    return sync_popular_movies(pages=pages)

@router.post("/full")
def sync_full(
    pages: int = 5,
    cast_limit: int = 1000,
    actor_details_limit: int = 1000,
):
    return sync_full_database(
        pages=pages,
        cast_limit=cast_limit,
        actor_details_limit=actor_details_limit,
    )