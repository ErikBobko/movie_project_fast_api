import pandas as pd

def build_movie_dataframe(filtered_movies):
    df = pd.DataFrame(filtered_movies)

    expected_cols = [
        "id",
        "tmdb_id",
        "title",
        "year",
        "rating",
        "popularity",
        "vote_count",
        "original_language",
        "runtime",
        "category",
        "poster_path",
        "overview",
    ]

    for col in expected_cols:
        if col not in df.columns:
            df[col] = None

    df = df[expected_cols]

    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["decade"] = (df["year"] // 10) * 10

    return df