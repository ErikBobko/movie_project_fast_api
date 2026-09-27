from db import  supabase



def fetch_top_actors_by_movie_count():
    response = (
        supabase
        .table("actor_movie_counts")
        .select("*")
        .order("movie_count", desc=True)
        .limit(10)
        .execute()
    )

    return response.data


def fetch_highest_rated_actors():
    response = (
        supabase
        .table("actor_rating_stats")
        .select("*")
        .gte("movie_count", 25)
        .order("avg_rating", desc=True)
        .limit(10)
        .execute()
    )

    return response.data


def fetch_most_popular_actors():
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

def fetch_actors_for_best_score():
    response = (
        supabase
        .table("actor_rating_stats")
        .select("*")
        .gte("movie_count", 4)
        .execute()
    )

    return response.data