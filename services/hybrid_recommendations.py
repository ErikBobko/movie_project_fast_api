from services.similar_movies import get_similar_movies
from services.content_recommendations import get_similar_movies_by_content


def get_hybrid_similar_movies(movie_id: int, limit: int = 10):
    metadata_results = get_similar_movies(movie_id)
    content_results = get_similar_movies_by_content(movie_id, limit=30)

    combined = {}

    for movie in metadata_results:
        movie_id_key = movie["id"]

        combined[movie_id_key] = {
            **movie,
            "metadata_score": movie.get("similarity_score", 0),
            "content_score": 0,
        }

    for movie in content_results:
        movie_id_key = movie["id"]

        if movie_id_key not in combined:
            combined[movie_id_key] = {
                **movie,
                "metadata_score": 0,
                "content_score": movie.get("content_similarity", 0),
            }
        else:
            combined[movie_id_key]["content_score"] = movie.get(
                "content_similarity",
                0
            )

    for movie in combined.values():
        metadata_score = movie.get("metadata_score", 0)
        content_score = movie.get("content_score", 0) * 100

        movie["hybrid_score"] = round(
            metadata_score * 0.4 + content_score * 0.6,
            2
        )

    results = sorted(
        combined.values(),
        key=lambda movie: movie["hybrid_score"],
        reverse=True
    )

    return results[:limit]