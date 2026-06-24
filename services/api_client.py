
API_URL = "http://127.0.0.1:8000"
import streamlit as st
import requests

@st.cache_data(ttl=3600, show_spinner=False)
def get_actor(tmdb_actor_id: int):
    try:
        response = requests.get(f"{API_URL}/actors/{tmdb_actor_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
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
@st.cache_data(ttl=3600, show_spinner=False)
def get_movie_cast(tmdb_id: int):
    response = requests.get(f"{API_URL}/movies/{tmdb_id}/cast")
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=3600, show_spinner=False)
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