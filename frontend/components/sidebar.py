
import streamlit as st


PAGES = [
    ("Career Match AI", "🎯"),
    ("Resume Report", "📄"),
    ("Interview IQ", "🎙"),
    ("AI STAR Enhancer", "✨"),
]


def render_sidebar():

    with st.sidebar:

        st.markdown(
            '<div class="brand">⚡ Career<span>Match</span></div>',
            unsafe_allow_html=True
        )

        st.caption("WORKSPACE")

        current = st.session_state.get(
            "page", "Career Match AI"
        )

        options = [page[0] for page in PAGES]

        selected = st.radio(
            "Navigation",
            options,
            index=options.index(current),
            format_func=lambda value: (
                dict(PAGES)[value] + "  " + value
            ),
            label_visibility="collapsed",
            key="navigation"
        )

        st.divider()

        st.caption("PREFERENCES")

        current_theme = st.session_state.get(
            "theme", "Light"
        )

        theme = st.selectbox(
            "Appearance",
            ["Light", "Dark"],
            index=0 if current_theme == "Light" else 1,
            key="sidebar_theme"
        )

        if theme != current_theme:
            st.session_state.theme = theme
            st.rerun()

        st.divider()

        st.markdown(
            """
            <div class="status">
                <span class="status-dot"></span>
                System Operational
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Career Match AI v2.0")

    return selected
