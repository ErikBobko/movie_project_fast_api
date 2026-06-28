
API_URL = "http://127.0.0.1:8000"

import requests


def get_actor(tmdb_actor_id: int):
    try:
        response = requests.get(f"{API_URL}/actors/{tmdb_actor_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_movie_crew(tmdb_id: int):
    try:
        response = requests.get(f"{API_URL}/movies/{tmdb_id}/crew", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {
            "directors": [],
            "writers": [],
            "composers": []
        }

def get_movie_cast(tmdb_id: int):
    response = requests.get(f"{API_URL}/movies/{tmdb_id}/cast")
    response.raise_for_status()
    return response.json()

def get_actor_movies(tmdb_actor_id: int):
    try:
        response = requests.get(f"{API_URL}/actors/{tmdb_actor_id}/movies", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def get_movie_by_id(movie_id: int):
    try:
        response = requests.get(f"{API_URL}/movies/by-id/{movie_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def get_actor_analytics():
    try:
        response = requests.get(f"{API_URL}/analytics/actors", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def get_top_actors():
    try:
        response = requests.get(
            f"{API_URL}/analytics/actors/top",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return []

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