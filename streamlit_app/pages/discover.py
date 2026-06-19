import streamlit as st
import random


def render_discover(movies):

    st.subheader("🎬 Discover Movies")

    mode = st.selectbox(
        "Choose mode",
        ["Random", "Top Rated", "Hidden Gems"]
    )

    # =========================
    # RANDOM
    # =========================

    if "random_movie" not in st.session_state:
        st.session_state.random_movie = random.choice(movies)

    if mode == "Random":

        m = st.session_state.random_movie

        col1, col2 = st.columns([8, 1])

        with col1:
            st.markdown(f"### 🎬 {m.get('title')}")
            st.write(f"⭐ Rating: {m.get('rating')}")

        with col2:
            if st.button("🎲", help="Random movie"):
                st.session_state.random_movie = random.choice(movies)
                st.rerun()

    # =========================
    # TOP RATED
    # =========================

    elif mode == "Top Rated":

        result = sorted(
            [
                m for m in movies
                if m.get("vote_count", 0) >= 10000
            ],
            key=lambda x: x.get("rating", 0),
            reverse=True
        )[:5]

        st.markdown("---")

        for movie in result:
            st.write(
                f"🎬 {movie.get('title')} "
                f"(⭐ {movie.get('rating')})"
            )

    # =========================
    # HIDDEN GEMS
    # =========================

    elif mode == "Hidden Gems":

        result = sorted(
            [
                m for m in movies
                if m.get("rating", 0) >= 7
            ],
            key=lambda x: x.get("rating", 0),
            reverse=True
        )[:5]

        st.markdown("---")

        for movie in result:
            st.write(
                f"💎 {movie.get('title')} "
                f"(⭐ {movie.get('rating')})"
            )