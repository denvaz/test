import streamlit as st
from utils import hide_sidebar_page, login, sidebar_logged_in, SessionState
import streamlit.components.v1 as components
def main():
    st.set_page_config(page_title="Method", layout="wide")

    st.markdown("""
        <style>
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)

    hide_sidebar_page()

    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    if not st.session_state.session_state.logged_in:
        login()
    else:
        sidebar_logged_in()
# PAGE CONTENT GOES HERE #################################################################
        st.header(':rainbow[DASHBOARD]', divider='rainbow')
        st.title(':green[Coming soon...]')
        with open('receipt.html', 'r') as file:
            receipt_html = file.read()

        components.html(receipt_html)


if __name__ == "__main__":
    main()
