import streamlit as st

def render_kpis(total_movies, avg_rating, avg_popularity, languages_count):
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("🎬 Movies", total_movies)
    k2.metric("⭐ Avg Rating", round(avg_rating, 2))
    k3.metric("📈 Avg Popularity", round(avg_popularity, 2))
    k4.metric("🌍 Languages", languages_count)