from db import supabase


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