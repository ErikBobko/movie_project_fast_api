from fastapi import APIRouter
from models.movie import Movie
from services.movies import (get_all_movies,get_movie_by_id,get_movie_by_tmdb_id,create_movie)
from clients.tmdb_client import (get_movie_cast,get_movie_crew_summary)
router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("")
def get_movies(limit: int = 100,offset: int = 0):
    """
    Vráti zoznam filmov

    :param limit:  max.počet filmov
    :param offset:  od ktorého záznamu začíname

    """
    return get_all_movies(limit=limit,offset=offset)

@router.get("/by-tmdb-id/{tmdb_id}")
def movie_by_tmdb_id(tmdb_id: int):
    return get_movie_by_tmdb_id(tmdb_id)

@router.get("/by-id/{movie_id}")
def movie_by_id(movie_id: int):
    return get_movie_by_id(movie_id)

@router.get("/{tmdb_id}/cast}")
def get_cast(tmdb_id: int):
    return get_movie_cast(tmdb_id)

@router.get("/{tmdb_id}/crew}")
def get_crew(tmdb_id: int):
    return get_movie_crew_summary(tmdb_id)

@router.post("")
def create_new_movie(movie: Movie):
    return create_movie(movie)