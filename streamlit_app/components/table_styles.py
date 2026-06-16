def style_movie_table(df):
    return (
        df.style
        .format({
            "rating": "{:.2f}",
            "year": "{:.0f}",
            "popularity": "{:.1f}",
            "runtime": "{:.0f}"
        })
        .map(lambda x: "color: #00C49F", subset=["rating"])
        .map(lambda x: "color: #FFD166", subset=["year"])
        .map(lambda x: "color: #60A5FA", subset=["popularity"])
    )