def calculate_metrics(filtered_movies):
    total_movies = len(filtered_movies)

    avg_rating = (
        sum(m.get("rating") or 0 for m in filtered_movies)
        / total_movies
        if total_movies
        else 0
    )

    avg_popularity = (
        sum(m.get("popularity") or 0 for m in filtered_movies)
        / total_movies
        if total_movies
        else 0
    )

    return {
        "total_movies": total_movies,
        "avg_rating": avg_rating,
        "avg_popularity": avg_popularity,
    }