
import os
import time
import requests

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def get_similar_movies(movie_id: int):
    response = requests.get(f"{API_URL}/movies/{movie_id}/similar")
    response.raise_for_status()
    return response.json()

def safe_get(url, timeout=75, retries=2, **kwargs):
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                timeout=timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"Request failed ({attempt + 1}/{retries}): {url}")

            if attempt < retries - 1:
                time.sleep(0.5)

    return None

def get_actor(tmdb_actor_id: int):
    return safe_get(
        f"{API_URL}/actors/{tmdb_actor_id}"
    )

def get_movie_crew(tmdb_id: int):
    data = safe_get(
        f"{API_URL}/movies/{tmdb_id}/crew"
    )

    return data or {
        "directors": [],
        "writers": [],
        "composers": [],
    }

def get_movie_cast(tmdb_id: int):
    data = safe_get(
        f"{API_URL}/movies/{tmdb_id}/cast"
    )

    return data or []


def get_actor_movies(tmdb_actor_id: int):
    data = safe_get(
        f"{API_URL}/actors/{tmdb_actor_id}/movies"
    )

    return data or []

def get_movie_by_id(movie_id: int):
    return safe_get(
        f"{API_URL}/movies/by-id/{movie_id}"
    )


def get_actor_analytics():
    try:
        response = requests.get(f"{API_URL}/analytics/actors", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def get_top_actors():
    return safe_get(
        f"{API_URL}/analytics/actors/top",
        timeout=10
    ) or []

def get_highest_rated_actors():
    try:
        response = requests.get(
            f"{API_URL}/analytics/actors/highest-rated",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return []

def get_most_popular_actors():
    try:
        response = requests.get(
            f"{API_URL}/analytics/actors/popular",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return []

def get_all_actors(limit: int = 50, search: str | None = None):
    try:
        params = {"limit": limit}

        if search:
            params["search"] = search

        response = requests.get(
            f"{API_URL}/actors",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def get_best_actors():
    try:
        response = requests.get(
            f"{API_URL}/analytics/actors/best",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return []

def get_ai_recommendations(prompt: str):
    response = requests.post(
        f"{API_URL}/ai/recommendations",
        json={"prompt": prompt}
    )
    response.raise_for_status()
    return response.json()

def get_all_movies(page_size: int = 1000) -> list[dict]:
    movies = []
    offset = 0

    while True:
        batch = safe_get(
            f"{API_URL}/movies",
            params={
                "limit": page_size,
                "offset": offset,
            },
            timeout=75,
        )

        movies.extend(batch)

        if len(batch) < page_size:
            break

        offset += page_size

    return movies