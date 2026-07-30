from db import supabase


def get_movie_ids_by_actor(actor_name: str) -> list[int]:
    """
    Return IDs of movies connected to actors whose name matches actor_name.

    The actor search is case-insensitive and allows partial matching.
    """
    if not actor_name or not actor_name.strip():
        return []

    actor_response = (
        supabase
        .table("actors")
        .select("id, name")
        .ilike("name", f"%{actor_name.strip()}%")
        .limit(10)
        .execute()
    )

    actors = actor_response.data or []

    if not actors:
        return []

    actor_ids = [
        actor["id"]
        for actor in actors
        if actor.get("id") is not None
    ]

    if not actor_ids:
        return []

    movie_actor_response = (
        supabase
        .table("movie_actors")
        .select("movie_id")
        .in_("actor_id", actor_ids)
        .execute()
    )

    movie_actor_rows = movie_actor_response.data or []

    return list({
        row["movie_id"]
        for row in movie_actor_rows
        if row.get("movie_id") is not None
    })


def get_actor_names_by_movie_ids(movie_ids: list[int]) -> dict[int, list[str]]:
    """
    Return actor names grouped by movie ID.

    Example:
    {
        123: ["Brad Pitt", "Sandra Bullock"],
        456: ["Another Actor"]
    }
    """
    if not movie_ids:
        return {}

    movie_actor_response = (
        supabase
        .table("movie_actors")
        .select("movie_id, actor_id")
        .in_("movie_id", movie_ids)
        .execute()
    )

    relations = movie_actor_response.data or []

    if not relations:
        return {}

    actor_ids = list({
        row["actor_id"]
        for row in relations
        if row.get("actor_id") is not None
    })

    if not actor_ids:
        return {}

    actors_response = (
        supabase
        .table("actors")
        .select("id, name")
        .in_("id", actor_ids)
        .execute()
    )

    actors = actors_response.data or []

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
    year: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    actor: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """
    Return movies matching all supplied filters.

    year:
        Exact year, for example 2020.

    year_from:
        Minimum year, inclusive.

    year_to:
        Maximum year, inclusive.
    """
    safe_limit = max(1, min(int(limit or 10), 100))

    query = (
        supabase
        .table("movies")
        .select("*")
        .gte("rating", float(min_rating or 0))
        .not_.is_("rating", "null")
    )

    if year is not None:
        query = query.eq("year", int(year))
    else:
        if year_from is not None:
            query = query.gte("year", int(year_from))

        if year_to is not None:
            query = query.lte("year", int(year_to))

    if actor:
        movie_ids = get_movie_ids_by_actor(actor)

        if not movie_ids:
            return []

        query = query.in_("id", movie_ids)

    # Fetch enough candidates for local genre filtering and score sorting.
    response = query.limit(1000).execute()
    movies = response.data or []

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

    for movie in movies:
        movie["recommendation_score"] = calculate_recommendation_score(movie)

    movies.sort(
        key=lambda movie: movie["recommendation_score"],
        reverse=True,
    )

    selected_movies = movies[:safe_limit]

    # Add verified actor names so the AI explanation does not have to guess.
    selected_movie_ids = [
        movie["id"]
        for movie in selected_movies
        if movie.get("id") is not None
    ]

    actors_by_movie = get_actor_names_by_movie_ids(selected_movie_ids)

    for movie in selected_movies:
        movie["actors"] = actors_by_movie.get(movie.get("id"), [])

    return selected_movies