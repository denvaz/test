import streamlit as st
from utils import hide_sidebar_page, login, sidebar_logged_in, SessionState

st.markdown("""
    <style>
        margin-top: -220px;
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

hide_sidebar_page()

# Create session state object
if 'session_state' not in st.session_state:
    st.session_state.session_state = SessionState()

if not st.session_state.session_state.logged_in:
    login()
else:
    sidebar_logged_in()
# PAGE CONTENT GOES HERE #################################################################
    st.header(f'Hi :red[ {st.session_state.session_state.user}]!', divider='red')