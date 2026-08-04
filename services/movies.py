"""Služba pre čítanie a vytváranie filmov v databáze.

Tento modul spravuje len databázové operácie pre tabuľku movies.
Nespravuje TMDB klienta, neukladá externé dáta a neobsahuje
logiku odporúčaní. Súvisiaca obchodná logika patrí do služieb
alebo pipeline.
"""

from db import supabase
from models.movie import Movie


def get_all_movies(limit: int = 100, offset: int = 0):
    safe_limit = max(1, min(limit, 1000))
    safe_offset = max(0, offset)

    response = (
        supabase
        .table("movies")
        .select("*")
        .range(
            safe_offset,
            safe_offset + safe_limit - 1,
        )
        .execute()
    )

    return response.data or []


def get_movie_by_tmdb_id(tmdb_id: int):
    response = (
        supabase
        .table("movies")
        .select("*")
        .eq("tmdb_id", tmdb_id)
        .maybe_single()
        .execute()
    )

    return response.data


def create_movie(movie: Movie):
    response = supabase.table("movies").insert(movie.model_dump()).execute()
    return response.data


def get_movie_by_id(movie_id: int):
    response = (
        supabase
        .table("movies")
        .select("*")
        .eq("id", movie_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]