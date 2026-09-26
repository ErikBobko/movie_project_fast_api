from fastapi import APIRouter

from services.actors import (get_actor_by_tmdb_id,get_actor_movies_by_tmdb_id,get_all_actors)

router = APIRouter(prefix="/actors", tags=["Actors"])

@router.get("")
def all_actors(limit: int = 50,search: str | None = None ):
    return get_all_actors(limit=limit, search=search)

@router.get("/{tmdb_actor_id}")
def get_actor(tmdb_actor_id: int):
    return get_actor_by_tmdb_id(tmdb_actor_id)

@router.get("/{tmdb_actor_id}/movies")
def get_actor_movies(tmdb_actor_id: int):
    return get_actor_movies_by_tmdb_id(tmdb_actor_id)