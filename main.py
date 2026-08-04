"""Hlavný FastAPI vstupný bod projektu.

Tento súbor definuje HTTP endpointy a deleguje prácu do služieb.
Nedrží obchodné pravidlá ani databázovú logiku priamo v routech.
Súvisiace operácie patria do služieb a pipeline.
"""
from fastapi import FastAPI
from models.movie import Movie
from clients.tmdb_client import get_movie_cast, get_movie_crew_summary
from pipelines.ingestion import sync_popular_movies
from pipelines.full_sync import sync_full_database
from pipelines.cast_sync import sync_movie_casts, sync_missing_movie_casts, sync_actor_details
from services.actors import get_actor_by_tmdb_id, get_actor_movies_by_tmdb_id, get_all_actors
from services.movies import get_all_movies, get_movie_by_id, get_movie_by_tmdb_id, create_movie
from services.actor_analytics import get_top_actors_by_movie_count, get_highest_rated_actors, get_most_popular_actors, get_best_actors
from services.analytics import get_top_rated, get_language_stats
from services.recommendations import get_recommendations
from services.similar_movies import get_similar_movies
from services.content_recommendations import get_similar_movies_by_content
from services.hybrid_recommendations import get_hybrid_similar_movies
from services.ai_recommendations import parse_user_prompt, get_ai_recommendations
from models.ai import PromptRequest

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Movie API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analytics/top-rated")
def top_rated():
    return get_top_rated()

@app.get("/analytics/actors/popular")
def most_popular_actors():
    return get_most_popular_actors()

@app.get("/analytics/languages")
def languages():
    return get_language_stats()

@app.get("/movies")
def get_movies():
    return get_all_movies()

@app.get("/movies/by-tmdb-id/{tmdb_id}")
def movie_by_tmdb_id(tmdb_id: int):
    return get_movie_by_tmdb_id(tmdb_id)

@app.get("/movies/{tmdb_id}/cast")
def get_cast(tmdb_id: int):
    return get_movie_cast(tmdb_id)

@app.get("/movies/{tmdb_id}/crew")
def get_crew(tmdb_id: int):
    return get_movie_crew_summary(tmdb_id)

@app.get("/actors")
def all_actors(limit: int = 50, search: str | None = None):
    return get_all_actors(limit=limit, search=search)

@app.get("/actors/{tmdb_actor_id}")
def get_actor(tmdb_actor_id: int):
    return get_actor_by_tmdb_id(tmdb_actor_id)

@app.get("/actors/{tmdb_actor_id}/movies")
def get_actor_movies(tmdb_actor_id: int):
    return get_actor_movies_by_tmdb_id(tmdb_actor_id)

@app.get("/movies/by-id/{movie_id}")
def movie_by_id(movie_id: int):
    return get_movie_by_id(movie_id)

@app.post("/sync/casts")
def sync_casts(limit: int = 100, offset: int = 0):
    return sync_movie_casts(limit=limit, offset=offset)

@app.post("/movies")
def create_new_movie(movie: Movie):
    return create_movie(movie)

@app.post("/sync/casts/missing")
def sync_missing_casts(limit: int = 100):
    return sync_missing_movie_casts(limit)

@app.get("/analytics/actors/top")
def top_actors():
    return get_top_actors_by_movie_count()

@app.get("/analytics/actors/highest-rated")
def highest_rated_actors():
    return get_highest_rated_actors()

@app.post("/sync/popular")
def sync_movies(pages: int = 1):
    return sync_popular_movies(pages=pages)

@app.get("/analytics/actors/best")
def best_actors():
    return get_best_actors()

@app.post("/sync/actors/details")
def sync_actors_details(limit: int = 100):
    return sync_actor_details(limit)

@app.post("/sync/full")
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

@app.get("/recommendations")
def recommendations(
    genre: str | None = None,
    min_rating: float = 0,
    min_vote_count: int = 100,
    year: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    actor: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    limit: int = 10,
):
    return get_recommendations(
        genre=genre,
        min_rating=min_rating,
        min_vote_count=min_vote_count,
        year=year,
        year_from=year_from,
        year_to=year_to,
        actor=actor,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
    )

@app.get("/movies/{movie_id}/similar")
def similar_movies(movie_id: int):
    return get_similar_movies(movie_id)

@app.get("/movies/{movie_id}/similar/content")
def similar_movies_by_content(movie_id: int, limit: int = 10):
    return get_similar_movies_by_content(movie_id, limit)

@app.get("/movies/{movie_id}/similar/hybrid")
def hybrid_similar_movies(movie_id: int, limit: int = 10):
    return get_hybrid_similar_movies(movie_id, limit)

@app.post("/ai/parse")
def ai_parse(request: PromptRequest):
    return parse_user_prompt(request.prompt)

@app.post("/ai/recommendations")
def ai_recommendations(request: PromptRequest):
    return get_ai_recommendations(request.prompt)