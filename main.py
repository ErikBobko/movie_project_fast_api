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

@app.post("/movies")
def create_movie(movie: Movie):
    response = supabase.table("movies").insert(movie.model_dump()).execute()
    return response.data

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

@app.post("/sync/popular")
def sync_movies():
    return sync_popular_movies()

@app.get("/movies/{tmdb_id}/crew")
def get_crew(tmdb_id: int):
    return get_movie_crew_summary(tmdb_id)