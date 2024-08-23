import streamlit as st
from st_pages import hide_pages
from supabase import create_client, Client

# Class for managing session state
class SessionState:
    def __init__(self):
        self.logged_in = False
        self.user = None
def logout():
    st.session_state.session_state.logged_in = False

def login():
    loginform = st.container()
    with loginform:
        l, c, r = st.columns([2, 1, 2])
        with c:
            cloginform = st.container(border=True)
            with cloginform:
                st.header('Sign in')
                login = st.text_input('Login')
                password = st.text_input('Passowrd', type='password')
                if st.button('Sign in'):
                    supabase = init_supabase()
                    response = supabase.table("users").select("username").filter("username", "eq", login).filter("password", "eq", password).execute()
                    if response.data and len(response.data) > 0:
                        st.session_state.session_state.logged_in = True
                        st.session_state.session_state.user = login
                        st.experimental_rerun()
                    else:
                        st.error('invalid login or password')

def sidebar_logged_in():
    # st.markdown("""
    #     <style>
    #         section[data-testid="stSidebar"][aria-expanded="true"]{
    #             display: block;
    #         }
    #     </style>
    #     """, unsafe_allow_html=True)
     
    LOGO = "images/rbaselogo.png"
    # st.logo(LOGO)
    with st.sidebar:
        st.page_link("Rbase.py",label="Main",icon="🔘",use_container_width=True)
        st.page_link("pages/dashboard.py",label=" Dashboard",icon="🔘",use_container_width=True)
        st.page_link("pages/task_tracking.py",label=" Adressess",icon="🔘",use_container_width=True)
        st.subheader("SN", divider="gray")
        st.page_link("pages/check_sn.py",label=" Check SN",icon="🔘",use_container_width=True)
        st.page_link("pages/new_sn.py",label=" New SN list",icon="🔘",use_container_width=True)
        st.page_link("pages/used_sn.py",label=" Used SN list",icon="🔘",use_container_width=True)
        st.subheader("Receipt", divider="gray")
        st.page_link("pages/amazon_receipt_gen.py",label=" Amazon receipt",icon="🔘",use_container_width=True)
        st.subheader("Tools", divider="gray")
        st.page_link("pages/pack_tracking.py",label=" Pack tracking",icon="🔘",use_container_width=True)
        st.page_link("pages/metadata_clean.py",label=" Metadata cleaner",icon="🔘",use_container_width=True)
        st.subheader("")
        st.subheader("")
        st.button('Exit', on_click = logout)

def init_supabase():
    url = "https://ekphnccyjmmoohivjxsu.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrcGhuY2N5am1tb29oaXZqeHN1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3MDI5MzMsImV4cCI6MjAzNzI3ODkzM30.1_kMU3S8vJlVDFkm8ro2CGvNKSy_PGeCK4FsLxXnDpU"
    return create_client(url, key)


