import streamlit as st
import pandas as pd

from services.analytics import get_kpis
from services.analytics import get_top_rated
from services.analytics import get_movies

st.set_page_config(
    page_title="Movie Analytics",
    layout="wide"
)

st.title("🎬 Movie Analytics Dashboard")

st.sidebar.header("Filters")

# -----------------
# DATA LOAD
# -----------------
kpis = get_kpis()
movies = get_movies()

# -----------------
# FILTERS SECTION
# -----------------

years = sorted(
    set(movie["year"] for movie in movies if movie["year"] is not None)
)

selected_year = st.sidebar.selectbox(
    "Year",
    options=["All"] + years
)

min_rating = st.sidebar.slider(
    "Minimum rating",
    0.0,
    10.0,
    0.0,
    0.5
)

# apply filters
filtered_movies = movies

if selected_year != "All":
    filtered_movies = [
        m for m in filtered_movies if m["year"] == selected_year
    ]

filtered_movies = [
    m for m in filtered_movies if m["rating"] >= min_rating
]

top_movies_filtered = sorted(
    filtered_movies,
    key=lambda x: x["rating"],
    reverse=True
)[:10]

# -----------------
# KPI SECTION
# -----------------

col1, col2 = st.columns(2)

col1.metric(
    "Total Movies",
    kpis["total_movies"]
)

col2.metric(
    "Average Rating",
    round(kpis["avg_rating"], 2)
)

# -----------------
# TABLES SECTION
# -----------------

st.subheader("⭐ Top Rated Movies (Filtered)")
st.dataframe(pd.DataFrame(top_movies_filtered))

st.subheader("🎥 Movies")

df = pd.DataFrame(filtered_movies)
st.dataframe(df)