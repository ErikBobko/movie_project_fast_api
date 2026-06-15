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