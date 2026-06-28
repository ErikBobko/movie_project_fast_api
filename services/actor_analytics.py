from db import supabase


def get_actor_analytics():
    response = (
        supabase
        .table("movie_actors")
        .select(
            """
            id,
            character,
            cast_order,
            actors (
                id,
                tmdb_actor_id,
                name,
                profile_path
            ),
            movies (
                id,
                tmdb_id,
                title,
                rating,
                popularity,
                year
            )
            """
        )
        .execute()
    )

    return response.data