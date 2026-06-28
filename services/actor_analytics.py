from db import supabase


def get_top_actors_by_movie_count():
    response = (
        supabase
        .table("movie_actors")
        .select(
            """
            actor_id,
            actors (
                name
            )
            """
        )
        .execute()
    )

    data = response.data

    actor_counts = {}

    for row in data:
        actor = row["actors"]

        if not actor:
            continue

        name = actor["name"]

        actor_counts[name] = actor_counts.get(name, 0) + 1

    result = [
        {"name": name, "movie_count": count}
        for name, count in actor_counts.items()
    ]

    result.sort(
        key=lambda x: x["movie_count"],
        reverse=True
    )

    return result[:10]

def get_highest_rated_actors():
    response = (
        supabase
        .table("movie_actors")
        .select(
            """
            actor_id,
            actors (
                name
            ),
            movies (
                rating
            )
            """
        )
        .execute()
    )

    data = response.data

    actor_stats = {}

    for row in data:
        actor = row.get("actors")
        movie = row.get("movies")

        if not actor or not movie:
            continue

        name = actor.get("name")
        rating = movie.get("rating")

        if name is None or rating is None:
            continue

        if name not in actor_stats:
            actor_stats[name] = {
                "name": name,
                "movie_count": 0,
                "rating_sum": 0,
            }

        actor_stats[name]["movie_count"] += 1
        actor_stats[name]["rating_sum"] += rating

    result = []

    for actor in actor_stats.values():
        if actor["movie_count"] < 2:
            continue

        avg_rating = actor["rating_sum"] / actor["movie_count"]

        result.append({
            "name": actor["name"],
            "movie_count": actor["movie_count"],
            "avg_rating": round(avg_rating, 2),
        })

    result.sort(
        key=lambda x: x["avg_rating"],
        reverse=True
    )

    return result[:10]

def get_most_popular_actors():
    response = (
        supabase
        .table("movie_actors")
        .select(
            """
            actor_id,
            actors (
                name
            ),
            movies (
                popularity
            )
            """
        )
        .execute()
    )

    data = response.data

    actor_stats = {}

    for row in data:
        actor = row.get("actors")
        movie = row.get("movies")

        if not actor or not movie:
            continue

        name = actor.get("name")
        popularity = movie.get("popularity")

        if name is None or popularity is None:
            continue

        if name not in actor_stats:
            actor_stats[name] = {
                "name": name,
                "movie_count": 0,
                "popularity_sum": 0,
            }

        actor_stats[name]["movie_count"] += 1
        actor_stats[name]["popularity_sum"] += popularity

    result = []

    for actor in actor_stats.values():

        if actor["movie_count"] < 2:
            continue

        avg_popularity = (
            actor["popularity_sum"] /
            actor["movie_count"]
        )

        result.append({
            "name": actor["name"],
            "movie_count": actor["movie_count"],
            "avg_popularity": round(avg_popularity, 2)
        })

    result.sort(
        key=lambda x: x["avg_popularity"],
        reverse=True
    )

    return result[:10]