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