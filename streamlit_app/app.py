import streamlit as st
from services.analytics import get_movies
from services.filters import  filter_movies
from components.charts import  render_movies_per_year, render_rating_split, render_top_genres
from services.metrics import calculate_metrics
from components.kpis import  render_kpis
from services.dataframe_builder import build_movie_dataframe
from services.charts_data import build_charts_data

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

from components.sidebar import render_sidebar

with st.sidebar:
    filters = render_sidebar(movies)

year_range = filters["year_range"]
min_rating = filters["min_rating"]
min_votes = filters["min_votes"]

# =========================
# FILTERING
# =========================

filtered_movies = filter_movies(
    movies,
    year_range,
    min_rating,
    min_votes
)

if not filtered_movies:
    st.warning("No movies match the selected filters.")
    st.stop()

# =========================
# KPI
# =========================

metrics = calculate_metrics(filtered_movies)

total_movies = metrics["total_movies"]
avg_rating = metrics["avg_rating"]
avg_popularity = metrics["avg_popularity"]

# =========================
# DATAFRAME SAFE CONVERSION
# =========================

df = build_movie_dataframe(filtered_movies)

# =========================
# DERIVED DATA
# =========================

chart_df, rating_split, genre_df = build_charts_data(df)


# =========================
# UI
# =========================
main = st.container()

with main:
    st.title("🍿 Movie Analytics Dashboard")


    st.markdown(
        """
        <p style="
            color:#9CA3AF;
            font-size:16px;
            margin-top:-20px;
            margin-bottom:30px;
        ">
            Insights into movie trends, ratings and popularity
        </p>
        """,
        unsafe_allow_html=True
    )

    # KPI
    k1, k2, k3, k4 = st.columns(4)

    render_kpis(
        total_movies,
        avg_rating,
        avg_popularity,
        df["original_language"].nunique()
    )

    st.markdown("---")

    # CHARTS
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            render_movies_per_year(chart_df)

    with c2:
        with st.container(border=True):
            render_rating_split(rating_split)

    with c3:
        with st.container(border=True):
            render_top_genres(genre_df)

    st.markdown("---")

    # TABLES SAFE
    top_movies = df.sort_values("rating", ascending=False).head(10)
    popular_movies = df.sort_values("popularity", ascending=False).head(10)


    t1, t2 = st.columns(2)

    with t1:
        st.subheader("Top Rated Movies")

        top_movies_styled = (
            top_movies.style
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

        st.dataframe(top_movies_styled, width="stretch")

    with t2:
        st.subheader("Most Popular Movies")

        popular_movies_styled = (
            popular_movies.style
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

        st.dataframe(popular_movies_styled, width="stretch")

    st.markdown("---")

    st.subheader("All Movies")

    page_size = 20

    total_pages = max(1, (len(df) - 1) // page_size + 1)

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1,
        step=1
    )

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    paged_df = df.iloc[start_idx:end_idx]

    paged_df_styled = (
        paged_df.style
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

    st.dataframe(paged_df_styled, width="stretch")

    st.caption(f"Page {page} of {total_pages}")
