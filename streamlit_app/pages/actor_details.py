import streamlit as st


def render_actor_details(actor_id):
    if st.button("⬅ Back to movie"):
        st.session_state.app_mode = "detail"
        st.session_state.selected_actor_id = None
        st.rerun()

    st.title("Actor Detail")
    st.write(f"Actor ID: {actor_id}")