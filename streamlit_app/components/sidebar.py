def render_sidebar(movies):
    import streamlit as st
    from streamlit_option_menu import option_menu
    from streamlit_app.pages.render_filters import render_filters_section
    from streamlit_app.pages.discover import render_discover

    st.markdown("## 🎬 Movie Dashboard")

    section = option_menu(
        menu_title=None,
        options=["Overview", "Search", "Filters", "Discover", "About"],
        icons=["house", "search", "funnel", "stars", "info-circle"],
        default_index=0,
        orientation="vertical",
    )

    # DEFAULT STATE
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None

    if "filters" not in st.session_state:
        st.session_state.filters = {
            "year_range": (1900, 2100),
            "min_rating": 0.0,
            "min_votes": 0,
        }

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    search_query = st.session_state.search_query

    # OVERVIEW
    if section == "Overview":
        st.subheader("Dataset Overview")
        st.write(f"Movies loaded: {len(movies)}")

    # SEARCH
    elif section == "Search":
        st.subheader("🔎 Search Movies")

        search_query = st.text_input("Search by title", key="search_query")
        search_query = st.session_state.search_query

    # FILTERS
    elif section == "Filters":
        filters = render_filters_section(movies)
        st.session_state.filters = filters

    # ABOUT
    elif section == "About":
        st.subheader("About")
        st.write("TMDB API")
        st.write("Supabase")

    return section, search_query, st.session_state.filters