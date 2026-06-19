import streamlit as st

def render_movie_details(movie_id, df):

    movie = df[df["id"] == movie_id].iloc[0]

    st.title(movie["title"])

    col1, col2 = st.columns([1, 3])

    with col1:
        if movie.get("poster_path"):
            poster_url = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
            st.image(poster_url)

    with col2:
        st.subheader("Overview")
        st.write(movie.get("overview", "No overview available"))

        st.write(f"⭐ Rating: {movie['rating']}")
        st.write(f"🎬 Year: {movie['year']}")
        st.write(f"🔥 Popularity: {movie['popularity']}")