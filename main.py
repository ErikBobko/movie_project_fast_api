"""
FASTAPI ENTRY POINT

Úloha:
- spúšťa backend server
- definuje API endpointy
- prepája services (analytics, ingestion)
- vystavuje dáta pre Streamlit alebo iné klienty

Dôležité:
- NEobsahuje business logiku
- NErobí výpočty
- IBA volá services
"""
from services.ingestion import  sync_popular_movies
from fastapi import FastAPI
from services.analytics import get_movies, get_top_rated, get_language_stats
from db import supabase
from pydantic import BaseModel
from models.movie import Movie

app = FastAPI()

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

@app.post("/sync/popular")
def sync_movies():
    return sync_popular_movies()