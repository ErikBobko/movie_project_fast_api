"""
ANALYTICS SERVICE

Úloha:
- načítava dáta z databázy
- pripravuje analytické výstupy
- poskytuje dáta pre API a Streamlit

Dôležité:
- neposiela requesty do TMDB
- nemení dáta v databáze
- pracuje iba s uloženými dátami
"""

from db import supabase
API_URL = "http://127.0.0.1:8000"
import requests

def get_movie_cast(tmdb_id: int):
    response = requests.get(f"{API_URL}/movies/{tmdb_id}/cast")
    response.raise_for_status()
    return response.json()


def get_top_rated(limit=10):
    response = supabase.table("movies") \
        .select("*") \
        .order("rating", desc=True) \
        .limit(limit) \
        .execute()

    return response.data


"""KOLKO FILMOV JE V KAŽDOM JAZYKU"""


def get_language_stats():
    response = supabase.table("movies").select("*").limit(1).execute()
    return response.data


def get_movies():
    response = (
        supabase
        .table("movies")
        .select("*")
        .range(0, 11000)
        .execute()
    )

    return response.data

def get_movies_count():
    response = (
        supabase
        .table("movies")
        .select("*", count="exact")
        .execute()
    )

    return response.count

def get_kpis():
    movies = get_movies()

    total_movies = get_movies_count()

    avg_rating = (
        sum(movie["rating"] for movie in movies)
        / len(movies)
        if movies
        else 0
    )

    return {
        "total_movies": total_movies,
        "avg_rating": avg_rating
    }


def get_movie_crew(tmdb_id: int):
    try:
        response = requests.get(f"{API_URL}/movies/{tmdb_id}/crew", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {
            "directors": [],
            "writers": [],
            "composers": []
        }

def get_actor(tmdb_actor_id: int):
    try:
        response = requests.get(f"{API_URL}/actors/{tmdb_actor_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_actor_movies(tmdb_actor_id: int):
    try:
        response = requests.get(f"{API_URL}/actors/{tmdb_actor_id}/movies", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def get_movie_by_id(movie_id: int):
    try:
        response = requests.get(f"{API_URL}/movies/by-id/{movie_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None