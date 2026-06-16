import pandas as pd

def build_charts_data(df):
    chart_df = (
        df.groupby("decade")
        .size()
        .reset_index(name="count")
    )

    rating_df = df.dropna(subset=["rating"]).copy()

    def rating_bucket(r):
        if r >= 8:
            return "High (8+)"
        elif r >= 6:
            return "Medium (6-7.9)"
        else:
            return "Low (<6)"

    rating_df["rating_group"] = rating_df["rating"].apply(rating_bucket)

    rating_split = (
        rating_df["rating_group"]
        .value_counts()
        .reset_index()
    )
    rating_split.columns = ["group", "count"]

    genres = []
    if "category" in df.columns:
        for categories in df["category"].dropna():
            genres.extend([g.strip() for g in categories.split(",")])

        genre_df = (
            pd.Series(genres)
            .value_counts()
            .head(5)
            .reset_index()
        )
        genre_df.columns = ["genre", "count"]
    else:
        genre_df = pd.DataFrame()

    return chart_df, rating_split, genre_df