import streamlit as st
# from utils import hide_sidebar_page, login, sidebar_logged_in, SessionState
from utils import login, sidebar_logged_in, SessionState
st.set_page_config(page_title="Amazon receipt", layout="wide")

# Create session state object
if 'session_state' not in st.session_state:
    st.session_state.session_state = SessionState()

if not st.session_state.session_state.logged_in:
    login()
else:
    sidebar_logged_in()
# PAGE CONTENT GOES HERE #################################################################
    st.header(f'Hi :red[ {st.session_state.session_state.user}]!', divider='red')