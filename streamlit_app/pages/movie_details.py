import streamlit as st
from services.analytics import get_movie_cast,get_movie_crew



def render_movie_details(movie_id, df):
    if st.button("⬅ Back to movies"):
        st.session_state.selected_movie_id = None
        st.session_state.app_mode = "list"
        st.rerun()

    movie = df[df["id"] == movie_id].iloc[0]
    cast = get_movie_cast(movie["tmdb_id"])
    crew = get_movie_crew(movie["tmdb_id"])

    st.title(movie["title"])

    col1, col2 = st.columns([1, 3])

    with col1:
        if movie.get("poster_path"):
            poster_url = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
            st.image(poster_url)

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
                profile_path = actor.get("profile_path")

                if profile_path:
                    profile_url = f"https://image.tmdb.org/t/p/w185{profile_path}"
                    st.image(profile_url, width=80)
                else:
                    st.write("🎭")

            with col_info:
                st.markdown(f"**{actor.get('name', 'Unknown actor')}**")
                st.caption(f"as {actor.get('character', 'Unknown role')}")

