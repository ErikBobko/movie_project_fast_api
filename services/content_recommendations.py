from db import supabase
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_movies_with_overview():
    response = (
        supabase
        .table("movies")
        .select("id, title, overview, rating, year, category, poster_path")
        .not_.is_("overview", "null")
        .range(0, 11000)
        .execute()
    )

    return response.data or []


def get_similar_movies_by_content(movie_id: int, limit: int = 10):
    movies = get_movies_with_overview()

    if not movies:
        return []

    movie_index = None

    for index, movie in enumerate(movies):
        if movie["id"] == movie_id:
            movie_index = index
            break

    if movie_index is None:
        return []

    overviews = [
        movie.get("overview") or ""
        for movie in movies
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(overviews)

    similarity_scores = cosine_similarity(
        tfidf_matrix[movie_index],
        tfidf_matrix
    ).flatten()

    similar_indices = similarity_scores.argsort()[::-1]

    results = []

    for index in similar_indices:
        movie = movies[index]

        if movie["id"] == movie_id:
            continue

        results.append({
            "id": movie["id"],
            "title": movie["title"],
            "rating": movie.get("rating"),
            "year": movie.get("year"),
            "category": movie.get("category"),
            "poster_path": movie.get("poster_path"),
            "content_similarity": round(float(similarity_scores[index]), 4),
        })

        if len(results) >= limit:
            break

    return results