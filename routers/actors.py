from fastapi import APIRouter,HTTPException,Path,Query

from services.actors import (get_actor_by_tmdb_id,get_actor_movies_by_tmdb_id,get_all_actors)

router = APIRouter(prefix="/actors", tags=["Actors"])


@router.get("")
def all_actors(
    limit: int = Query(default=50, ge=1, le=100),
    search: str | None = None
):
    return get_all_actors(limit=limit, search=search)


@router.get("/{tmdb_actor_id}")
def get_actor(tmdb_actor_id: int = Path(gt = 0) ):
    actor = get_actor_by_tmdb_id(tmdb_actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor


@router.get("/{tmdb_actor_id}/movies")
def get_actor_movies(tmdb_actor_id:  int = Path(gt = 0)):
    actor = get_actor_by_tmdb_id(tmdb_actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return get_actor_movies_by_tmdb_id(tmdb_actor_id)