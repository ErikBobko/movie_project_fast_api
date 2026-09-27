from repositories.analytics import fetch_top_rated


def get_top_rated(limit: int = 10):
    return fetch_top_rated(limit)