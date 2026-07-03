import streamlit as st
from services.api_client import get_movie_cast,get_movie_crew
from services.api_client import get_movie_by_id
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
NO_POSTER_PATH = BASE_DIR / "assets" / "no_poster.png"



def render_movie_details(movie_id):
    if st.session_state.get("previous_actor_id"):
        if st.button("⬅ Back to actor", key="back_to_actor_from_movie_detail"):
            st.session_state.selected_movie_id = None
            st.session_state.selected_actor_id = st.session_state.previous_actor_id
            st.session_state.previous_actor_id = None
            st.session_state.app_mode = "actor_detail"
            st.rerun()
    else:
        if st.button("⬅ Back to movies", key="back_to_movies_from_detail"):
            st.session_state.selected_movie_id = None
            st.session_state.app_mode = "list"
            st.rerun()

    movie = get_movie_by_id(movie_id)


    if not movie:
        st.error(f"Movie not found. movie_id={movie_id}")
        return

    poster_path = movie.get("poster_path")

    cast = get_movie_cast(movie["tmdb_id"])
    crew = get_movie_crew(movie["tmdb_id"])

    st.title(movie["title"])

    col1, col2 = st.columns([1, 3])

    with col1:
        poster_path = movie.get("poster_path")

        if poster_path and isinstance(poster_path, str) and poster_path.startswith("/"):
            st.image(
                f"https://image.tmdb.org/t/p/w300{poster_path}",
                width=300
            )
        else:
            st.image(
                str(NO_POSTER_PATH),
                width=300
            )

    with col2:
        st.subheader("Overview")
        st.write(movie.get("overview", "No overview available"))

        st.markdown(f"""
        ### {movie['title']}

        ⭐ **Rating:** {movie['rating']:.2f}  
        📅 **Year:** {int(movie['year'])}  
        🔥 **Popularity:** {movie['popularity']:.1f}

        ---
        """)

    st.markdown("---")
    st.subheader("Crew")

    directors = crew.get("directors", [])
    writers = crew.get("writers", [])
    composers = crew.get("composers", [])

    if directors:
        st.write(f"🎬 Director: {', '.join(directors)}")

    if writers:
        st.write(f"✍️ Writer: {', '.join(writers)}")

    if composers:
        st.write(f"🎵 Composer: {', '.join(composers)}")

    st.markdown("---")
    st.subheader("Cast")

    if not cast:
        st.write("No cast available.")
    else:
        for actor in cast:
            col_img, col_info = st.columns([1, 5])

            with col_img:
                render_small_actor_image(actor.get("profile_path"), width=80)

            with col_info:
                actor_name = actor.get("name", "Unknown actor")
                actor_id = actor.get("id")

                if actor_id:
                    if st.button(actor_name, key=f"actor_{actor_id}_{movie_id}"):
                        st.session_state.selected_actor_id = actor_id
                        st.session_state.app_mode = "actor_detail"
                        st.session_state.previous_page = "movie_detail"
                        st.session_state.previous_section = st.session_state.get(
                            "active_section",
                            "Overview"
                        )
                        st.rerun()
                else:
                    st.markdown(f"**{actor_name}**")

                character = actor.get("character")

                if character:
                    st.caption(f"as {character}")

            st.markdown(
                "<div style='margin-bottom:22px;'></div>",
                unsafe_allow_html=True
            )

def render_small_actor_image(profile_path, width=70):
    if profile_path:
        image_url = f"https://image.tmdb.org/t/p/w185{profile_path}"
        st.image(image_url, width=width)
    else:
        st.markdown(
            f"""
            <div style="
                width:{width}px;
                height:{int(width * 1.45)}px;
                border-radius:8px;
                background:#1F2937;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:28px;
                color:#9CA3AF;
                border:1px solid #374151;
            ">
                🎭
            </div>
            """,
            unsafe_allow_html=True
        )
