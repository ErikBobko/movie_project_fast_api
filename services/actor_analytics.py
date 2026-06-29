from db import supabase
import math

def get_top_actors_by_movie_count():
    response = (
        supabase
        .table("actor_movie_counts")
        .select("*")
        .order("movie_count", desc=True)
        .limit(10)
        .execute()
    )

    return response.data


def get_highest_rated_actors():
    response = (
        supabase
        .table("actor_rating_stats")
        .select("*")
        .gte("movie_count", 4)
        .order("avg_rating", desc=True)
        .limit(10)
        .execute()
    )

    return response.data


def get_most_popular_actors():
    response = (
        supabase
        .table("actor_popularity_stats")
        .select("*")
        .gte("movie_count", 4)
        .order("avg_popularity", desc=True)
        .limit(10)
        .execute()
    )

    return response.data

def get_best_actors():
    response = (
        supabase
        .table("actor_rating_stats")
        .select("*")
        .gte("movie_count", 4)
        .execute()
    )

    actors = response.data

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