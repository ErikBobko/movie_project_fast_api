import streamlit as st

from services.analytics import get_kpis
from services.analytics import get_top_rated

st.set_page_config(
    page_title="Movie Analytics",
    layout="wide"
)

st.title("🎬 Movie Analytics Dashboard")


top_movies = get_top_rated()
kpis = get_kpis()

col1, col2 = st.columns(2)

col1.metric(
    "Total Movies",
    kpis["total_movies"]
)

col2.metric(
    "Average Rating",
    round(kpis["avg_rating"], 2)
)


st.subheader("⭐ Top Rated Movies")
st.dataframe(top_movies)