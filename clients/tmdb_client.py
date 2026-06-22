"""
TMDB MODULE

Úloha:
- komunikuje s TMDB API (The Movie Database)
- sťahuje surové dáta o filmoch

Dôležité:
- NEpracuje s databázou
- NErobí analýzy
- NEobsahuje business logiku

Je to API client pre TMDB.
"""

import requests
from config import TMDB_API_KEY
from services.analytics import get_movie_cast

BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies(page: int = 1):
    response = requests.get(
        f"{BASE_URL}/movie/popular",
        params={
            "api_key": TMDB_API_KEY,
            "page": page
        }
    )
    return response.json()["results"]

def get_now_playing_movies():
    url = f"{BASE_URL}/movie/now_playing"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["results"]

def get_genres():
    url = f"{BASE_URL}/genre/movie/list"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()["genres"]

def get_movie_details(tmdb_id: int):
    return requests.get(
        f"{BASE_URL}/movie/{tmdb_id}",
        params={"api_key": TMDB_API_KEY}
    ).json()


def get_movie_credits(tmdb_id: int):
    response = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/credits",
        params={
            "api_key": TMDB_API_KEY,
            "language": "en-US",
        }
    )
    response.raise_for_status()
    return response.json()


def get_movie_cast(tmdb_id: int, limit: int = 10):
    credits = get_movie_credits(tmdb_id)
    cast = credits.get("cast", [])

    return [
        {
            "id": actor.get("id"),
            "name": actor.get("name"),
            "character": actor.get("character"),
            "profile_path": actor.get("profile_path"),
            "order": actor.get("order"),
        }
        for actor in cast[:limit]
    ]

def get_movie_crew_summary(tmdb_id: int):
    credits = get_movie_credits(tmdb_id)
    crew = credits.get("crew", [])

    directors = [
        person.get("name")
        for person in crew
        if person.get("job") == "Director"
    ]

    writers = [
        person.get("name")
        for person in crew
        if person.get("department") == "Writing"
    ]

    composers = [
        person.get("name")
        for person in crew
        if person.get("job") == "Original Music Composer"
    ]

    return {
        "directors": list(dict.fromkeys(directors)),
        "writers": list(dict.fromkeys(writers)),
        "composers": list(dict.fromkeys(composers)),
    }