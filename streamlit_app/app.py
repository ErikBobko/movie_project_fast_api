import streamlit as st
import pandas as pd
from services.analytics import get_movies

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Movie Dashboard", layout="wide")

# =========================
# LOAD DATA
# =========================
movies = get_movies()

if not movies:
    st.error("No movies loaded")
    st.stop()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("? Movie Analytics")

    years = sorted({m.get("year") for m in movies if m.get("year") is not None})

    selected_year = st.selectbox("Year", ["All"] + years)
    min_rating = st.slider("Minimum Rating", 0.0, 10.0, 5.0)
    min_votes = st.slider("Minimum Votes", 0, 10000, 100)

# =========================
# FILTERING
# =========================
filtered_movies = movies

if selected_year != "All":
    filtered_movies = [
        m for m in filtered_movies
        if m.get("year") == selected_year
    ]

filtered_movies = [
    m for m in filtered_movies
    if (m.get("rating") or 0) >= min_rating
]

filtered_movies = [
    m for m in filtered_movies
    if (m.get("vote_count") or 0) >= min_votes
]

# =========================
# KPI
# =========================
total_movies = len(filtered_movies)

avg_rating = (
    sum(m.get("rating") or 0 for m in filtered_movies) / total_movies
    if total_movies else 0
)

avg_popularity = (
    sum(m.get("popularity") or 0 for m in filtered_movies) / total_movies
    if total_movies else 0
)

# =========================
# DATAFRAME SAFE CONVERSION
# =========================
df = pd.DataFrame(filtered_movies)


expected_cols = ["title",  "year", "rating","popularity","vote_count","original_language","runtime"]

for col in expected_cols:
    if col not in df.columns:
        df[col] = None

df = df[expected_cols]

# =========================
# DERIVED DATA
# =========================
chart_df = df.groupby("year").size().reset_index(name="count")

lang_df = pd.DataFrame(filtered_movies)

if "original_language" in lang_df.columns:
    lang_df = lang_df["original_language"].value_counts().reset_index()
    lang_df.columns = ["language", "count"]
else:
    lang_df = pd.DataFrame(columns=["language", "count"])

genre_df = pd.DataFrame()

if "category" in pd.DataFrame(filtered_movies).columns:

    genres = []

    for categories in pd.DataFrame(filtered_movies)["category"].dropna():
        genres.extend([g.strip() for g in categories.split(",")])

    genre_df = (
        pd.Series(genres)
        .value_counts()
        .head(20)
        .reset_index()
    )

    genre_df.columns = ["genre", "count"]

# =========================
# UI
# =========================
main = st.container()

with main:

    st.title("? Movie Analytics Dashboard")

    # KPI
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Movies", total_movies)
    k2.metric("Avg Rating", round(avg_rating, 2))
    k3.metric("Avg Popularity", round(avg_popularity, 2))
    k4.metric("Languages", len(lang_df))

    st.markdown("---")

    # CHARTS
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Movies per Year")

        if not chart_df.empty:
            st.bar_chart(chart_df.set_index("year"))

    with c2:
        st.subheader("Language Distribution")

        if not lang_df.empty:
            st.bar_chart(lang_df.set_index("language"))

    with c3:
        st.subheader("Top 10 Genres")

        if not genre_df.empty:
            st.bar_chart(genre_df.set_index("genre"))

    st.markdown("---")

    # TABLES SAFE
    top_movies = df.sort_values("rating", ascending=False).head(10)
    popular_movies = df.sort_values("popularity", ascending=False).head(10)

    t1, t2 = st.columns(2)

    with t1:
        st.subheader("Top Rated Movies")
        st.dataframe(top_movies, width="stretch")

    with t2:
        st.subheader("Most Popular Movies")
        st.dataframe(popular_movies, width="stretch")

    st.markdown("---")

    st.subheader("All Movies")
    st.dataframe(df, width="stretch")