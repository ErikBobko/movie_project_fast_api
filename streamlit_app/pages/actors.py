import streamlit as st
import pandas as pd
import plotly.express as px

from services.api_client import get_top_actors


def render_actors_page():
    st.title("🎭 Actor Analytics")
    st.caption("Insights into cast appearances, ratings and popularity")

    actors = get_top_actors()

    if not actors:
        st.warning("No actor analytics data available.")
        return

    df = pd.DataFrame(actors)

    top_actor = df.iloc[0]["name"]
    top_actor_movies = df.iloc[0]["movie_count"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Top Actors", len(df))

    with col2:
        st.metric("Most Featured Actor", f"{top_actor} ({top_actor_movies})")

    st.divider()

    fig = px.bar(
        df,
        x="movie_count",
        y="name",
        orientation="h",
        title="Top 10 Actors by Movie Count",
        labels={
            "movie_count": "Movies",
            "name": "Actor"
        },
        text="movie_count",
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)