# streamlit_app/pages/recommendations.py

import random

def get_top_recommendations(movies, limit=5):
    return sorted(
        movies,
        key=lambda x: x.get("rating", 0),
        reverse=True
    )[:limit]


def get_random_recommendation(movies, limit=1):
    return random.sample(movies, min(limit, len(movies)))