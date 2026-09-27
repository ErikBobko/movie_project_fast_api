from db import supabase


def fetch_movies_with_overview():
    response = (
        supabase
        .table("movies")
        .select("id, title, overview, rating, year, category, poster_path")
        .not_.is_("overview", "null")
        .range(0, 11000)
        .execute()
    )

    return response.data or []