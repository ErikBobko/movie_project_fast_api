def filter_movies(
    movies,
    year_range,
    min_rating,
    min_votes
):
    return [
        m for m in movies
        if (
            m.get("year") is not None
            and year_range[0] <= m.get("year") <= year_range[1]
            and (m.get("rating") or 0) >= min_rating
            and (m.get("vote_count") or 0) >= min_votes
        )
    ]