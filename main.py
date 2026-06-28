"""
FASTAPI ENTRY POINT

Úloha:
- spúšťa backend server
- definuje API endpointy
- prepája služby a databázovú vrstvu
- vystavuje dáta pre Streamlit alebo iné klienty

Dôležité:
- neobsahuje business logiku
- nevykonáva analytické výpočty
- endpointy delegujú prácu na services alebo databázovú vrstvu
"""

from pipelines.ingestion import  sync_popular_movies
from fastapi import FastAPI
from services.analytics import  get_top_rated, get_language_stats
from db import supabase
from models.movie import Movie
from clients.tmdb_client import get_movie_cast, get_movie_crew_summary
from pipelines.cast_sync import sync_movie_casts , sync_missing_movie_casts
from services.actors import get_actor_by_tmdb_id, get_actor_movies_by_tmdb_id
from services.movies import get_movie_by_id
from services.actor_analytics import get_top_actors_by_movie_count,get_highest_rated_actors,get_most_popular_actors

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

@app.get("/analytics/languages")
def languages():
    return get_language_stats()

@app.get("/movies")
def get_movies():
    return supabase.table("movies").select("*").execute().data

@app.get("/movies/{tmdb_id}")
def get_movie(tmdb_id: int):
    print("tmdb_id:", tmdb_id, type(tmdb_id))
    return (supabase.table("movies").select("*").eq("tmdb_id", tmdb_id).maybe_single().execute().data )

@app.get("/movies/{tmdb_id}/cast")
def get_cast(tmdb_id: int):
    return get_movie_cast(tmdb_id)

@app.get("/movies/{tmdb_id}/crew")
def get_crew(tmdb_id: int):
    return get_movie_crew_summary(tmdb_id)

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

@app.post("/sync/popular")
def sync_movies():
    return sync_popular_movies()

@app.post("/movies")
def create_movie(movie: Movie):
    response = supabase.table("movies").insert(movie.model_dump()).execute()
    return response.data

@app.post("/sync/casts/missing")
def sync_missing_casts(limit: int = 100):
    return sync_missing_movie_casts(limit)

@app.get("/analytics/actors/top")
def top_actors():
    return get_top_actors_by_movie_count()

@app.get("/analytics/actors/highest-rated")
def highest_rated_actors():
    return get_highest_rated_actors()

@app.get("/analytics/actors/popular")
def most_popular_actors():
    return get_most_popular_actors()
