import streamlit as st
import pandas as pd
import plotly.express as px

from services.api_client import get_top_actors, get_highest_rated_actors,get_most_popular_actors,get_all_actors


def style_actor_table(df):
    styled = df.style

    format_dict = {}

    if "movie_count" in df.columns:
        format_dict["movie_count"] = "{:.0f}"

    if "avg_rating" in df.columns:
        format_dict["avg_rating"] = "{:.2f}"

    if "avg_popularity" in df.columns:
        format_dict["avg_popularity"] = "{:.2f}"

    styled = styled.format(format_dict, na_rep="")

    if "movie_count" in df.columns:
        styled = styled.set_properties(
            subset=["movie_count"],
            **{"color": "#60A5FA", "font-weight": "bold"}
        )

    if "avg_rating" in df.columns:
        styled = styled.set_properties(
            subset=["avg_rating"],
            **{"color": "#10B981", "font-weight": "bold"}
        )

    if "avg_popularity" in df.columns:
        styled = styled.set_properties(
            subset=["avg_popularity"],
            **{"color": "#10B981", "font-weight": "bold"}
        )

    return styled

def render_actors_page():
    st.title("🎭 Actor Analytics")
    st.caption("Insights into cast appearances, ratings and popularity")

    top_actors = get_top_actors()
    highest_rated_actors = get_highest_rated_actors()
    most_popular_actors = get_most_popular_actors()

    if not top_actors:
        st.warning("No actor analytics data available.")
        return

    top_df = pd.DataFrame(top_actors)
    rated_df = pd.DataFrame(highest_rated_actors)
    popular_df = pd.DataFrame(most_popular_actors)

    top_actor = top_df.iloc[0]["name"]
    top_actor_movies = top_df.iloc[0]["movie_count"]


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Top Actors", len(top_df))

    with col2:
        st.metric(
            "Most Featured Actor",
            f"{top_df.iloc[0]['name']} ({top_df.iloc[0]['movie_count']})"
        )

    with col3:
        st.metric(
            "Best Avg Rating",
            f"{rated_df.iloc[0]['avg_rating']}"
        )

    with col4:
        st.metric(
            "Highest Popularity",
            f"{popular_df.iloc[0]['avg_popularity']}"
        )

    st.divider()

    c1, c2, c3 = st.columns(3)

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
                color="movie_count",
                color_continuous_scale="Blues",
            )

            fig_top.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(fig_top, use_container_width=True)

    with c2:
        with st.container(border=True):
            fig_rated = px.bar(
                rated_df,
                x="avg_rating",
                y="name",
                orientation="h",
                title="Highest Rated Actors",
                text="avg_rating",
                color="avg_rating",
                color_continuous_scale="Greens",
            )

            fig_rated.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(
                fig_rated,
                use_container_width=True
            )

    with c3:
        with st.container(border=True):
            fig_popular = px.bar(
                popular_df,
                x="avg_popularity",
                y="name",
                orientation="h",
                title="Most Popular Actors",
                text="avg_popularity",
                color="avg_popularity",
                color_continuous_scale="Tealgrn",
            )

            fig_popular.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(
                fig_popular,
                use_container_width=True
            )

    with st.expander("Show raw analytics tables"):
        t1, t2, t3 = st.columns(3)

        with t1:
            st.subheader("Top Actors by Movie Count")
            st.dataframe(
                style_actor_table(top_df[["name", "movie_count"]]),
                use_container_width=True
            )

        with t2:
            st.subheader("Highest Rated Actors")
            st.dataframe(
                style_actor_table(rated_df[["name", "movie_count", "avg_rating"]]),
                use_container_width=True
            )

        with t3:
            st.subheader("Most Popular Actors")
            st.dataframe(
                style_actor_table(popular_df[["name", "movie_count", "avg_popularity"]]),
                use_container_width=True
            )

    st.divider()

    st.subheader("All Actors")

    actor_search = st.text_input(
        "Search actor",
        placeholder="Type actor name...",
        key="actor_search_query",
    )

    if not actor_search:
        st.info("Type an actor name to search.")
        return

    all_actors = get_all_actors(
        limit=50,
        search=actor_search,
    )

    if not all_actors:
        st.warning("No actors found.")
        return

    if len(actor_search) < 2:
        st.info("Type at least 2 letters to search.")
        return

    for actor in all_actors:
        col1, col2 = st.columns([1, 4])

        with col1:
            render_actor_image(actor.get("profile_path"), width=80)

        with col2:
            st.write(f"### {actor['name']}")

            if st.button(
                    "Actor Details",
                    key=f"actor_{actor['tmdb_actor_id']}"
            ):
                st.session_state.selected_actor_id = actor["tmdb_actor_id"]
                st.session_state.previous_page = "actors"
                st.session_state.active_section = "Actors"
                st.session_state.app_mode = "actor_detail"
                st.rerun()

def render_actor_image(profile_path, width=80):
    if profile_path:
        image_url = f"https://image.tmdb.org/t/p/w200{profile_path}"
        st.image(image_url, width=width)
    else:
        st.markdown(
            f"""
            <div style="
                width:{width}px;
                height:{int(width * 1.35)}px;
                border-radius:8px;
                background:#1F2937;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:32px;
                color:#9CA3AF;
                border:1px solid #374151;
            ">
                🎭
            </div>
            """,
            unsafe_allow_html=True
        )