"""
INGESTION SERVICE

Úloha:
- berie dáta z TMDB (cez tmdb.py)
- spracuje ich (minimalne čistenie / formátovanie)
- ukladá ich do databázy (db.py / Supabase)

Je to "pipeline" časť systému:
TMDB → ingestion → DB

Dôležité:
- NEkomunikuje priamo s FastAPI
- NEobsahuje UI logiku (Streamlit)
- NErobí analýzy (analytics.py)
"""

from clients.tmdb_client import (
    get_popular_movies,
    get_genres,
    get_movie_details,
)

from pipelines.movie_transformer import (build_genre_map, transform_movie)
from db import supabase

def sync_popular_movies(pages: int = 1):

    genres = get_genres()
    genre_map = build_genre_map(genres)

    all_movies = []

    for page in range(1, pages + 1):
        movies = get_popular_movies(page)

        for movie in movies:
            details = get_movie_details(movie["id"])

            transformed_movies = transform_movie(
                movie,
                genre_map,
                details
            )

            all_movies.append(transformed_movies)


    unique_movies = {}

    for movie in all_movies:
        unique_movies[movie["tmdb_id"]] = movie

    all_movies = list(unique_movies.values())

    response = (
        supabase
        .table("movies")

        .upsert(
            all_movies,
            on_conflict="tmdb_id"
        )
        .execute()
    )

    return response.data