import streamlit as st
import pandas as pd
import plotly.express as px

from services.api_client import get_top_actors, get_highest_rated_actors


def render_actors_page():
    st.title("🎭 Actor Analytics")
    st.caption("Insights into cast appearances, ratings and popularity")

    top_actors = get_top_actors()
    highest_rated_actors = get_highest_rated_actors()

    if not top_actors:
        st.warning("No actor analytics data available.")
        return

    top_df = pd.DataFrame(top_actors)
    rated_df = pd.DataFrame(highest_rated_actors)

    top_actor = top_df.iloc[0]["name"]
    top_actor_movies = top_df.iloc[0]["movie_count"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Top Actors", len(top_df))

    with col2:
        st.metric("Most Featured Actor", f"{top_actor} ({top_actor_movies})")

    with col3:
        if not rated_df.empty:
            best_actor = rated_df.iloc[0]["name"]
            best_rating = rated_df.iloc[0]["avg_rating"]
            st.metric("Best Avg Rating", f"{best_actor} ({best_rating})")
        else:
            st.metric("Best Avg Rating", "N/A")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            fig_top = px.bar(
                top_df,
                x="movie_count",
                y="name",
                orientation="h",
                title="Top 10 Actors by Movie Count",
                labels={
                    "movie_count": "Movies",
                    "name": "Actor",
                },
                text="movie_count",
            )

            fig_top.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(fig_top, use_container_width=True)

    with c2:
        with st.container(border=True):
            if not rated_df.empty:
                fig_rated = px.bar(
                    rated_df,
                    x="avg_rating",
                    y="name",
                    orientation="h",
                    title="Highest Rated Actors",
                    labels={
                        "avg_rating": "Average Rating",
                        "name": "Actor",
                    },
                    text="avg_rating",
                )

                fig_rated.update_layout(
                    yaxis={"categoryorder": "total ascending"}
                )

                st.plotly_chart(fig_rated, use_container_width=True)
            else:
                st.info("No highest rated actor data available.")

    st.divider()

    t1, t2 = st.columns(2)

    with t1:
        st.subheader("Top Actors by Movie Count")
        st.dataframe(top_df, use_container_width=True)

    with t2:
        st.subheader("Highest Rated Actors")
        st.dataframe(rated_df, use_container_width=True)