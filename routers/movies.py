from fastapi import APIRouter,Path,Query,HTTPException
from models.movie import Movie
from services.movies import (get_all_movies,get_movie_by_id,get_movie_by_tmdb_id,create_movie)
from clients.tmdb_client import (get_movie_cast,get_movie_crew_summary)


router = APIRouter(prefix="/movies", tags=["Movies"])

from fastapi import Query


@router.get("")
def get_movies(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    return get_all_movies(limit=limit, offset=offset)

@router.get("/by-tmdb-id/{tmdb_id}")
def movie_by_tmdb_id(tmdb_id: int = Path(ge=1)):
    movie = get_movie_by_tmdb_id(tmdb_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.get("/by-id/{movie_id}")
def movie_by_id(movie_id: int = Path(ge=1)):
    movie = get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie



@router.get("/{tmdb_id}/cast")
def get_cast(tmdb_id: int):
    return get_movie_cast(tmdb_id)

@router.get("/{tmdb_id}/crew")
def get_crew(tmdb_id: int):
    return get_movie_crew_summary(tmdb_id)

@router.post("")
def create_new_movie(movie: Movie):
    return create_movie(movie)

