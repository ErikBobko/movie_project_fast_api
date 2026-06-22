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
 NEobsahuje analytické výpočty
"""

from clients.tmdb_client import (
    get_popular_movies,
    get_genres,
    get_movie_details,
    get_movie_cast,
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

    saved_movies = response.data

    movie_id_by_tmdb_id = {
        movie["tmdb_id"]: movie["id"]
        for movie in saved_movies
    }

    for movie in saved_movies:
        tmdb_id = movie["tmdb_id"]
        db_movie_id = movie["id"]

        cast = get_movie_cast(tmdb_id, limit=10)

        for actor in cast:
            actor_payload = {
                "tmdb_actor_id": actor["id"],
                "name": actor["name"],
                "profile_path": actor["profile_path"],
            }

            actor_response = (
                supabase
                .table("actors")
                .upsert(
                    actor_payload,
                    on_conflict="tmdb_actor_id"
                )
                .execute()
            )

            saved_actor = actor_response.data[0]

            relation_payload = {
                "movie_id": db_movie_id,
                "actor_id": saved_actor["id"],
                "character": actor["character"],
                "cast_order": actor["order"],
            }

            supabase.table("movie_actors").upsert(
                relation_payload,
                on_conflict="movie_id,actor_id"
            ).execute()

    return {
        "movies_synced": len(saved_movies),
    }