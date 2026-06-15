import streamlit as st
import plotly.express as px


def render_movies_per_year(chart_df):
    st.subheader("Movies per Year")

    if chart_df.empty:
        return

    fig = px.bar(
        chart_df,
        x="decade",
        y="count",
        text="count",
        color="count",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, width="stretch")


def render_rating_split(rating_split):
    st.subheader("Rating Quality Split")

    if rating_split.empty:
        return

    fig = px.pie(
        rating_split,
        values="count",
        names="group",
        hole=0.4,
        color_discrete_sequence=[
            "#00C49F",
            "#F1C40F",
            "#E74C3C"
        ]
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color="#111",
                width=2
            )
        )
    )

    st.plotly_chart(fig, width="stretch")
