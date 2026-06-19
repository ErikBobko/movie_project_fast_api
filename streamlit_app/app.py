import streamlit as st

from services.analytics import get_movies
from services.filters import filter_movies
from components.charts import render_movies_per_year, render_rating_split, render_top_genres
from services.metrics import calculate_metrics
from components.kpis import render_kpis
from services.dataframe_builder import build_movie_dataframe
from services.charts_data import build_charts_data
from components.table_styles import style_movie_table
from components.sidebar import render_sidebar
from streamlit_app.pages.movie_details import render_movie_details


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Movie Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD DATA
# =========================
movies = get_movies()
if not movies:
    st.error("No movies loaded")
    st.stop()



# =========================
# STATE INIT
# =========================
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

if "filters" not in st.session_state:
    st.session_state.filters = {
        "year_range": (1900, 2100),
        "min_rating": 0.0,
        "min_votes": 0,
    }

if "app_mode" not in st.session_state:
    st.session_state.app_mode = "list"  # list | detail

# =========================
# ROUTING
# =========================
df = build_movie_dataframe(movies)
if st.session_state.app_mode == "detail":
    render_movie_details(st.session_state.selected_movie_id, df)
    st.stop()



# =========================
# SIDEBAR
# =========================

if st.session_state.app_mode == "list":
    with st.sidebar:
        section, search_query, filters = render_sidebar(movies)
else:
    search_query = None
    filters = st.session_state.filters

# =========================
# FILTERING (BASE FILTERS)
# =========================
filtered_movies = filter_movies(
    movies,
    filters["year_range"],
    filters["min_rating"],
    filters["min_votes"]
)

# search filter
if search_query:
    filtered_movies = [
        m for m in filtered_movies
        if search_query.lower() in m.get("title", "").lower()
    ]

if not filtered_movies:
    st.warning("No movies match the selected filters.")
    st.stop()


# =========================
# DATAFRAME SAFE CONVERSION
# =========================
df = build_movie_dataframe(filtered_movies)

# =========================
# KPI
# =========================
metrics = calculate_metrics(filtered_movies)

total_movies = metrics["total_movies"]
avg_rating = metrics["avg_rating"]
avg_popularity = metrics["avg_popularity"]


# =========================
# DERIVED DATA
# =========================
chart_df, rating_split, genre_df = build_charts_data(df)


# =========================
# UI
# =========================
main = st.container()

with main:
    st.title("? Movie Analytics Dashboard")

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

    if search_query:
        st.info(f"? Search results for: '{search_query}' ({len(filtered_movies)} movies)")


    # =========================
    # KPI
    # =========================
    k1, k2, k3, k4 = st.columns(4)
    render_kpis(
        total_movies,
        avg_rating,
        avg_popularity,
        df["original_language"].nunique()
    )

    st.markdown("---")


    # =========================
    # CHARTS
    # =========================
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


    # =========================
    # TABLES (TOP)
    # =========================
    top_movies = df[
        df["vote_count"] >= 10000
    ].sort_values("rating", ascending=False).head(10)

    popular_movies = df.sort_values("popularity", ascending=False).head(10)

    t1, t2 = st.columns(2)

    with t1:
        st.subheader("Top Rated Movies")
        st.dataframe(style_movie_table(top_movies), width="stretch")

    with t2:
        st.subheader("Most Popular Movies")
        st.dataframe(style_movie_table(popular_movies), width="stretch")

    st.markdown("---")


    # =========================
    # MOVIE LIST (CLICKABLE)
    # =========================
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

    for _, movie in paged_df.iterrows():

        col1, col2 = st.columns([1, 4])

        with col1:
            if movie.get("poster_path"):
                poster_url = f"https://image.tmdb.org/t/p/w200{movie['poster_path']}"
                st.image(poster_url, width=80)

        with col2:
            st.subheader(movie["title"])
            st.write(f"⭐ {movie['rating']} | 🎬 {movie['year']}")


            if st.button("Details", key=f"movie_{movie['id']}"):
                st.session_state.selected_movie_id = movie["id"]
                st.session_state.app_mode = "detail"
                st.rerun()

    st.caption(f"Page {page} of {total_pages}")