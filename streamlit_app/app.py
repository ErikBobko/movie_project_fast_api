import streamlit as st
import pandas as pd

st.set_page_config(page_title="Movie Dashboard", layout="wide")

# =========================
# SIDEBAR (FILTER PANEL)
# =========================
with st.sidebar:
    st.title("🎬 Movie Analytics")

    st.markdown("### Filters")

    selected_year = st.selectbox("Year", ["All", 2024, 2023, 2022])
    min_rating = st.slider("Minimum Rating", 0.0, 10.0, 5.0)
    min_votes = st.slider("Minimum Votes", 0, 10000, 100)

    st.markdown("---")
    st.info("Filter panel like in BI tools")


# =========================
# MAIN DATA (placeholder)
# =========================
# sem si napojíš svoje funkcie
# kpis = get_kpis()
# movies = get_movies()

total_movies = 5684
avg_rating = 6.72
avg_popularity = 27.45
total_votes = "12.45M"


# =========================
# MAIN DASHBOARD
# =========================
main = st.container()

with main:

    # =========================
    # TITLE
    # =========================
    st.title("📊 Movie Analytics Dashboard")
    st.markdown("TMDB Movie Data Analysis")

    # =========================
    # KPI ROW (5 cards ako na obrázku)
    # =========================
    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Total Movies", total_movies, "in database")
    k2.metric("Average Rating", avg_rating)
    k3.metric("Avg Popularity", avg_popularity)
    k4.metric("Total Votes", total_votes)
    k5.metric("Release Range", "1900 - 2024")

    st.markdown("---")


    # =========================
    # CHART ROW (3 GRID)
    # =========================
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Movies per Year")
        st.bar_chart(pd.DataFrame({
            "year": [2019, 2020, 2021, 2022],
            "count": [120, 150, 180, 210]
        }).set_index("year"))

    with c2:
        st.subheader("Language Distribution")
        st.bar_chart(pd.DataFrame({
            "lang": ["EN", "FR", "ES"],
            "count": [70, 20, 10]
        }).set_index("lang"))

    with c3:
        st.subheader("Rating Distribution")
        st.bar_chart(pd.DataFrame({
            "rating": [1,2,3,4,5,6,7,8,9,10],
            "count": [5,10,20,40,80,120,90,60,30,10]
        }).set_index("rating"))


    st.markdown("---")


    # =========================
    # TABLES SECTION (2 COLUMNS)
    # =========================
    t1, t2 = st.columns(2)

    with t1:
        st.subheader("Top Rated Movies")
        st.dataframe(pd.DataFrame({
            "Title": ["Movie A", "Movie B"],
            "Rating": [9.3, 9.1],
            "Year": [1994, 2001]
        }))

    with t2:
        st.subheader("Most Popular Movies")
        st.dataframe(pd.DataFrame({
            "Title": ["Movie X", "Movie Y"],
            "Popularity": [5000, 4800],
            "Year": [2020, 2021]
        }))


    st.markdown("---")


    # =========================
    # FULL TABLE (BOTTOM)
    # =========================
    st.subheader("All Movies")

    st.dataframe(pd.DataFrame({
        "Title": ["A", "B", "C"],
        "Rating": [8.1, 7.5, 9.0],
        "Year": [2001, 2005, 2010]
    }))