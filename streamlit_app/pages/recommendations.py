import streamlit as st

from services.api_client import get_ai_recommendations


def render_recommendations():
    st.title("🤖 AI Movie Recommendations")

    st.write(
        "Describe what kind of movie you want and AI will search only movies from your database."
    )

    prompt = st.text_area(
        "What would you like to watch?",
        placeholder="Example: Find me a sci-fi movie with Tom Hanks after 2010",
        height=120,
    )

    if st.button("Get recommendations"):
        if not prompt.strip():
            st.warning("Please enter what kind of movie you want.")
            return

        with st.spinner("Finding recommendations..."):
            result = get_ai_recommendations(prompt)

        filters = result.get("filters", {})
        recommendations = result.get("recommendations", [])

        st.subheader("AI understood this request as:")

        st.json(filters)

        st.markdown("---")
        st.subheader("Recommended movies")

        if not recommendations:
            st.info("No matching movies found.")
            return

        for movie in recommendations:
            col1, col2 = st.columns([1, 4])

            with col1:
                poster_path = movie.get("poster_path")

                if poster_path:
                    st.image(
                        f"https://image.tmdb.org/t/p/w200{poster_path}",
                        width=120
                    )
                else:
                    st.write("No poster")

            with col2:
                st.markdown(f"### {movie.get('title', 'Unknown title')}")

                st.write(
                    f"⭐ Rating: {movie.get('rating', 0):.2f} | "
                    f"📅 Year: {movie.get('year', 'N/A')}"
                )

                st.write(movie.get("overview", "No overview available."))

                ai_reason = movie.get("ai_reason")

                if ai_reason:
                    st.info(ai_reason)

            st.markdown("---")