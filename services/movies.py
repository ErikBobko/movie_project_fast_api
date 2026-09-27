
from models.movie import Movie
from repositories.movies import (
    fetch_all_movies,
    fetch_movie_by_tmdb_id,
    insert_movie,
    fetch_movie_by_id,
)



def get_all_movies(limit: int = 100, offset: int = 0):
    safe_limit = max(1, min(limit, 1000))
    safe_offset = max(0, offset)

    return fetch_all_movies(
        limit=safe_limit,
        offset=safe_offset,
    )


def get_movie_by_tmdb_id(tmdb_id: int):
    return fetch_movie_by_tmdb_id(tmdb_id)


def create_movie(movie: Movie):
    movie_data = movie.model_dump()

    return insert_movie(movie_data)


def get_movie_by_id(movie_id: int):
    return fetch_movie_by_id(movie_id)