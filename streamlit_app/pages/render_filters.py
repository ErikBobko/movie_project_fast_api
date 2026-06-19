import streamlit as st

def render_filters_section(movies):
    st.title("🎬 Movie Analytics")

    st.markdown("""
        <style>
        div[data-testid="stContainer"] {
            background: linear-gradient(135deg, #0f172a, #111827);
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 16px;
            backdrop-filter: blur(10px);
        }
        </style>
        """, unsafe_allow_html=True)

    years = sorted(
        {m.get("year") for m in movies if m.get("year") is not None}
    )

    min_year = min(years)
    max_year = max(years)

    year_range = st.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    min_rating = st.slider(
        "Minimum Rating",
        0.0,
        10.0,
        5.0
    )

    min_votes = st.slider(
        "Minimum Votes",
        0,
        10000,
        100
    )

    return {
        "year_range": year_range,
        "min_rating": min_rating,
        "min_votes": min_votes,
    }