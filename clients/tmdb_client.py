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