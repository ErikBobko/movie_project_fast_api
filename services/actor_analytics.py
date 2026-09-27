
import math

from repositories.actor_analytics import (
    fetch_top_actors_by_movie_count,
    fetch_highest_rated_actors,
    fetch_most_popular_actors,
    fetch_actors_for_best_score,
)



def get_top_actors_by_movie_count():
    return fetch_top_actors_by_movie_count()


def get_highest_rated_actors():
    return fetch_highest_rated_actors()


def get_most_popular_actors():
    return fetch_most_popular_actors()


def get_best_actors():
    actors = fetch_actors_for_best_score()

    for actor in actors:
        actor["actor_score"] = round(
            actor["avg_rating"] * math.log(actor["movie_count"] + 1),
            2
        )

    actors.sort(
        key=lambda actor: actor["actor_score"],
        reverse=True
    )

    return actors[:5]