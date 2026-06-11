"""
MOVIE TRANSFORMER

Úloha:
- berie surové dáta z TMDB API
- prekladá / mapuje ich do formy, ktorú očakáva databáza (Supabase)
- rieši rozdiely medzi TMDB štruktúrou a našou DB štruktúrou

Prečo existuje:
TMDB ≠ naša databáza
→ názvy polí sú iné
→ niektoré polia chýbajú
→ žánre sú len ID, nie text

Tento modul robí "preklad dát"
"""

def build_genre_map(genres):
    return {
        genre["id"]: genre["name"]
        for genre in genres
    }

def transform_movie(movie, genre_map, details=None):

    movie_genres = [
        genre_map[g]
        for g in movie["genre_ids"]
        if g in genre_map
    ]

    return {
        "title": movie["title"],
        "release_date": movie["release_date"]  or None,
        "tmdb_id": movie["id"],
        "rating": movie["vote_average"],
        "original_language": movie["original_language"],
        "popularity": movie["popularity"],
        "overview": movie["overview"],
        "vote_count": movie["vote_count"],
        "original_title": movie["original_title"],
        "year": int(movie["release_date"][:4]) if movie["release_date"] else None,
        "category": ", ".join(movie_genres),
        "runtime": details.get("runtime") if details else None,
        "poster_path": details.get("poster_path") if details else None,
    }