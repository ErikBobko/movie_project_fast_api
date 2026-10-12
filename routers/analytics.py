from fastapi import APIRouter,Query

from services.analytics import get_top_rated

from services.actor_analytics import (
    get_top_actors_by_movie_count,
    get_highest_rated_actors,
    get_most_popular_actors,
    get_best_actors,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/actors/top")
def top_rated(limit: int = Query(default = 10, ge = 1, le = 100)):
    return get_top_rated(limit)

@router.get("/actors/top")
def top_actors():
    return get_top_actors_by_movie_count()

@router.get("/actors/highest-rated")
def highest_rated_actors():
    return get_highest_rated_actors()

@router.get("/actors/popular")
def most_popular_actors():
    return get_most_popular_actors()

@router.get("/actors/best")
def best_actors():
    return get_best_actors()