
from repositories.recommendations import (
    fetch_actors_by_name,
    fetch_movie_ids_by_actor_ids,
    fetch_actor_relations_by_movie_ids,
    fetch_actors_by_ids,
    fetch_recommendation_candidates
)


def get_movie_ids_by_actor(actor_name: str) -> list[int]:
    if not actor_name or not actor_name.strip():
        return []

    actors = fetch_actors_by_name(actor_name.strip())

    if not actors:
        return []

    actor_ids = [
        actor["id"]
        for actor in actors
        if actor.get("id") is not None
    ]

    if not actor_ids:
        return []

    movie_actor_rows = fetch_movie_ids_by_actor_ids(actor_ids)

    return list({
        row["movie_id"]
        for row in movie_actor_rows
        if row.get("movie_id") is not None
    })



def get_actor_names_by_movie_ids(movie_ids: list[int]) -> dict[int, list[str]]:
    if not movie_ids:
        return {}

    relations = fetch_actor_relations_by_movie_ids(movie_ids)

    if not relations:
        return {}

    actor_ids = list({
        row["actor_id"]
        for row in relations
        if row.get("actor_id") is not None
    })

    if not actor_ids:
        return {}

    actors = fetch_actors_by_ids(actor_ids)

    actor_name_by_id = {
        actor["id"]: actor["name"]
        for actor in actors
        if actor.get("id") is not None and actor.get("name")
    }

    actors_by_movie: dict[int, list[str]] = {}

    for relation in relations:
        movie_id = relation.get("movie_id")
        actor_id = relation.get("actor_id")
        actor_name = actor_name_by_id.get(actor_id)

        if movie_id is None or not actor_name:
            continue

        actors_by_movie.setdefault(movie_id, []).append(actor_name)

    return actors_by_movie

def calculate_recommendation_score(movie: dict) -> float:
    rating = float(movie.get("rating") or 0)
    popularity = float(movie.get("popularity") or 0)
    vote_count = int(movie.get("vote_count") or 0)
    year = int(movie.get("year") or 0)

    score = 0.0

    score += rating * 10
    score += min(popularity, 500) * 0.05
    score += min(vote_count, 10000) * 0.002

    if year >= 2015:
        score += 5
    elif year >= 2000:
        score += 2

    return round(score, 2)




def get_recommendations(
    genre: str | None = None,
    min_rating: float = 0,
    min_vote_count: int = 100,
    year: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    actor: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    limit: int = 10,
) -> list[dict]:

    safe_limit = max(1, min(int(limit or 10), 100))

    movie_ids = None

    if actor:
        movie_ids = get_movie_ids_by_actor(actor)

        if not movie_ids:
            return []

    movies = fetch_recommendation_candidates(
        min_rating=float(min_rating or 0),
        min_vote_count=min_vote_count,
        year=int(year) if year is not None else None,
        year_from=int(year_from) if year_from is not None else None,
        year_to=int(year_to) if year_to is not None else None,
        movie_ids=movie_ids,
        limit=1000,
    )

    if genre:
        normalized_genre = genre.strip().casefold()

        movies = [
            movie
            for movie in movies
            if movie.get("category")
            and normalized_genre in str(movie["category"]).casefold()
        ]

    if not movies:
        return []

    if sort_by == "rating":
        movies.sort(
            key=lambda movie: float(movie.get("rating") or 0),
            reverse=sort_order != "asc",
        )

    elif sort_by == "popularity":
        movies.sort(
            key=lambda movie: float(movie.get("popularity") or 0),
            reverse=sort_order != "asc",
        )

    elif sort_by == "year":
        movies.sort(
            key=lambda movie: int(movie.get("year") or 0),
            reverse=sort_order != "asc",
        )

    else:
        for movie in movies:
            movie["recommendation_score"] = calculate_recommendation_score(movie)

        movies.sort(
            key=lambda movie: movie["recommendation_score"],
            reverse=True,
        )

    selected_movies = movies[:safe_limit]

    selected_movie_ids = [
        movie["id"]
        for movie in selected_movies
        if movie.get("id") is not None
    ]

    actors_by_movie = get_actor_names_by_movie_ids(selected_movie_ids)

    for movie in selected_movies:
        movie["actors"] = actors_by_movie.get(
            movie.get("id"),
            [],
        )

    return selected_movies