from db import supabase


def get_movie_ids_by_actor(actor_name: str):
    actor_response = (
        supabase
        .table("actors")
        .select("id, name")
        .ilike("name", f"%{actor_name}%")
        .limit(10)
        .execute()
    )

    actors = actor_response.data or []

    if not actors:
        return []

    actor_ids = [actor["id"] for actor in actors]

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
        if row.get("movie_id")
    })


def calculate_recommendation_score(movie):
    rating = movie.get("rating") or 0
    popularity = float(movie.get("popularity") or 0)
    vote_count = movie.get("vote_count") or 0
    year = movie.get("year") or 0

    score = 0

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
    year_from: int | None = None,
    actor: str | None = None,
    limit: int = 10,
):
    query = (
        supabase
        .table("movies")
        .select("*")
        .gte("rating", min_rating)
        .not_.is_("rating", "null")
    )

    if year_from:
        query = query.gte("year", year_from)

    if actor:
        movie_ids = get_movie_ids_by_actor(actor)

        if not movie_ids:
            return []

        query = query.in_("id", movie_ids)

    response = query.limit(1000).execute()
    movies = response.data or []

    if genre:
        movies = [
            movie for movie in movies
            if movie.get("category")
            and genre.lower() in movie["category"].lower()
        ]

    for movie in movies:
        movie["recommendation_score"] = calculate_recommendation_score(movie)

    movies = sorted(
        movies,
        key=lambda movie: movie["recommendation_score"],
        reverse=True
    )

    return movies[:limit]