import streamlit as st
from services.api_client import get_actor, get_actor_movies


def render_actor_details(tmdb_actor_id):
    if st.button("Back", key="actor_detail_back_button"):

        st.session_state.selected_actor_id = None

        if st.session_state.get("previous_page") == "actors":
            st.session_state.active_section = "Actors"
            st.session_state.app_mode = "list"

        elif st.session_state.get("previous_page") == "movie_detail":
            st.session_state.active_section = st.session_state.get(
                "previous_section",
                "Overview"
            )
            st.session_state.app_mode = "detail"

        st.rerun()

    actor = get_actor(tmdb_actor_id)
    movies = get_actor_movies(tmdb_actor_id)

    if not actor:
        st.error("Actor not found.")
        return

    col1, col2 = st.columns([1, 3])

    with col1:
        render_actor_profile_image(actor.get("profile_path"))

    with col2:
        st.title(actor.get("name", "Unknown actor"))
        st.write(f"Movies in database: **{len(movies)}**")

        ratings = [
            movie.get("rating")
            for movie in movies
            if movie.get("rating") is not None
        ]

        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            st.write(f"Average movie rating: **{avg_rating:.2f}**")

    st.markdown("---")
    st.subheader("Filmography in database")

    if not movies:
        st.write("No movies found for this actor.")
        return

    movies = sorted(
        movies,
        key=lambda movie: movie.get("release_date") or "",
        reverse=True
    )

    for movie in movies:
        col_img, col_info = st.columns([1, 5])

        with col_img:
            poster_path = movie.get("poster_path")

            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w185{poster_path}"
                st.image(poster_url, width=80)
            else:
                st.write("🎬")

        with col_info:
            st.markdown(f"**{movie.get('title', 'Unknown movie')}**")
            st.caption(
                f"⭐ {movie.get('rating', 'N/A')} | "
                f"📅 {movie.get('release_date', 'Unknown date')}"
            )


def render_actor_profile_image(profile_path):
    if profile_path:
        profile_url = f"https://image.tmdb.org/t/p/w300{profile_path}"
        st.image(profile_url)
    else:
        st.markdown(
            """
            <div style="
                width:220px;
                height:300px;
                border-radius:12px;
                background:#1F2937;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:72px;
                color:#9CA3AF;
                border:1px solid #374151;
            ">
                🎭
            </div>
            """,
            unsafe_allow_html=True
        )