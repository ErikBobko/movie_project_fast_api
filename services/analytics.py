"""
ANALYTICS SERVICE

Úloha:
- berie dáta z databázy (db.py / Supabase)
- počíta štatistiky a agregácie
- pripravuje dáta pre API alebo Streamlit

NEPOSIELA requesty do TMDB
NEUKLADÁ dáta
IBA spracováva už uložené dáta
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
        .limit(100)
        .execute()
    )

    return response.data