from fastapi import APIRouter

from services.similar_movies import get_similar_movies
from services.content_recommendations import get_similar_movies_by_content
from services.hybrid_recommendations import get_hybrid_similar_movies


router = APIRouter(prefix="/movies",tags=["Similar Movies"])

@router.get("/{movie_id}/similar")
def similar_movies(movie_id: int):
    return get_similar_movies(movie_id)

@router.get("/{movie_id}/similar/content")
def similar_movies_by_content(movie_id: int, limit: int = 10):
    return get_similar_movies_by_content(movie_id, limit)

@router.get("/{movie_id}/similar/hybrid")
def hybrid_similar_movies(movie_id: int, limit: int = 10):
    return get_hybrid_similar_movies(movie_id, limit)