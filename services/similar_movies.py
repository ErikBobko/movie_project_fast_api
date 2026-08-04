from db import supabase
from services.movies import get_movie_by_id


def get_movie_actor_ids(movie_id: int):
    response = (
        supabase
        .table("movie_actors")
        .select("actor_id")
        .eq("movie_id", movie_id)
        .execute()
    )

    return {
        row["actor_id"]
        for row in response.data
    }


def get_movies_by_actor_ids(actor_ids):
    response = (
        supabase
        .table("movie_actors")
        .select("movie_id, actor_id")
        .in_("actor_id", list(actor_ids))
        .execute()
    )

    return response.data


def get_similar_movies(movie_id: int):
    movie = get_movie_by_id(movie_id)

    if not movie:
        return []

    actor_ids = get_movie_actor_ids(movie_id)

    if not actor_ids:
        return []

    movie_actor_rows = get_movies_by_actor_ids(actor_ids)

    movie_scores = {}

    for row in movie_actor_rows:
        similar_movie_id = row["movie_id"]

        if similar_movie_id == movie_id:
            continue

        movie_scores[similar_movie_id] = (
            movie_scores.get(similar_movie_id, 0) + 1
        )

    sorted_movie_ids = sorted(
        movie_scores,
        key=movie_scores.get,
        reverse=True
    )[:10]

    movies = get_movies_by_ids(sorted_movie_ids)

    for movie_data in movies:
        shared_actor_count = movie_scores.get(
            movie_data["id"],
            0
        )

        movie_data["shared_actor_count"] = shared_actor_count

        movie_data["similarity_score"] = (
            calculate_similarity_score(
                movie,
                movie_data,
                shared_actor_count,
            )
        )

    for movie_data in movies:
        movie_data["shared_actor_count"] = movie_scores.get(
            movie_data["id"],
            0
        )

    movies = sorted(
        movies,
        key=lambda movie: movie["similarity_score"],
        reverse=True
    )
    return movies

def get_movies_by_ids(movie_ids):
    response = (
        supabase
        .table("movies")
        .select("*")
        .in_("id", movie_ids)
        .execute()
    )

    return response.data

def calculate_similarity_score(source_movie, candidate_movie, shared_actor_count):
    score = 0

    # spoloční herci
    score += shared_actor_count * 15

    # spoločné žánre
    source_genres = {
        genre.strip().lower()
        for genre in (source_movie.get("category") or "").split(",")
    }

    candidate_genres = {
        genre.strip().lower()
        for genre in (candidate_movie.get("category") or "").split(",")
    }

    shared_genres = source_genres.intersection(candidate_genres)

    score += len(shared_genres) * 10

    # podobný rating
    rating_diff = abs(
        (source_movie.get("rating") or 0)
        - (candidate_movie.get("rating") or 0)
    )

    score += max(0, 10 - rating_diff * 2)

    # podobný rok
    year_diff = abs(
        (source_movie.get("year") or 0)
        - (candidate_movie.get("year") or 0)
    )

    score += max(0, 10 - year_diff)

    return round(score, 2)