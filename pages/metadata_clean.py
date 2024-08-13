import streamlit as st
from utils import login, sidebar_logged_in, SessionState

# Основная часть приложения
def main():
    st.set_page_config(page_title="Method", layout="wide")

    # Create session state object
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    if not st.session_state.session_state.logged_in:
        login()
    else:
        sidebar_logged_in()
    st.title("Metadata cleaner")
    st.subheader("Upload file:")

    uploaded_file = st.file_uploader("Select file", type=["pdf"])

    # if uploaded_file is not None:
    #     if st.button("Clean"):
            
    #         st.success("Metadata cleaned!")
    #         st.subheader("Download cleaned image")

if __name__ == "__main__":
    main()
