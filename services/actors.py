
from repositories.actors import (
    fetch_actor_by_tmdb_id,
    fetch_movie_ids_by_actor_id,
    fetch_movies_by_ids,
    fetch_all_actors,
)


def get_actor_by_tmdb_id(tmdb_actor_id: int):
    return fetch_actor_by_tmdb_id(tmdb_actor_id)


def get_actor_movies_by_tmdb_id(tmdb_actor_id: int):
    actor = fetch_actor_by_tmdb_id(tmdb_actor_id)

    if not actor:
        return []

    movie_ids = fetch_movie_ids_by_actor_id(actor["id"])

    if not movie_ids:
        return []

    return fetch_movies_by_ids(movie_ids)



def get_all_actors(
    limit: int = 50,
    offset: int = 0,
    search: str | None = None
):
    return fetch_all_actors(
        limit=limit,
        offset=offset,
        search=search,
    )