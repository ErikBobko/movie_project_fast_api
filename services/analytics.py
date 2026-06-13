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
        .limit(1000)
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