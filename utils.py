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

    st.header('Sign in')
    login = st.text_input('Login')
    password = st.text_input('Passowrd', type='password')
    if st.button('Sign in'):
        # if st.button('Sign in'):
        supabase = init_supabase()
        response = supabase.table("users").select("username").filter("username", "eq", login).filter("password", "eq", password).execute()
        if response.data and len(response.data) > 0:
            st.session_state.session_state.logged_in = True
            st.session_state.session_state.user = login
            st.experimental_rerun()
        else:
            st.error('invalid login or password')

def hide_sidebar_page():
    hide_pages("Rbase")
    hide_pages("new_sn")
    hide_pages("used_sn")
    hide_pages("method")
    hide_pages("task_tracking")
    hide_pages("pack_tracking")
    hide_pages("tools")

def sidebar_logged_in():
    st.markdown("""
        <style>
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: block;
            }
        </style>
        """, unsafe_allow_html=True)
     
    LOGO = "images/rbaselogo.png"
    st.logo(LOGO)
    with st.sidebar:
        st.page_link("Rbase.py",label="Главная",icon="🔘",use_container_width=True)
        st.page_link("pages/task_tracking.py",label=" Задачи",icon="🔘",use_container_width=True)
        st.page_link("pages/new_sn.py",label=" Новые SN",icon="🔘",use_container_width=True)
        st.page_link("pages/used_sn.py",label=" Использованные SN",icon="🔘",use_container_width=True)
        st.page_link("pages/pack_tracking.py",label=" Трекинг паков",icon="🔘",use_container_width=True)
        st.page_link("pages/method.py",label=" Методы",icon="🔘",use_container_width=True)
        st.page_link("pages/tools.py",label=" Инструменты",icon="🔘",use_container_width=True)
        st.subheader("")
        st.subheader("")
        st.button('Выйти', on_click = logout)

def init_supabase():
    url = "https://ekphnccyjmmoohivjxsu.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrcGhuY2N5am1tb29oaXZqeHN1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3MDI5MzMsImV4cCI6MjAzNzI3ODkzM30.1_kMU3S8vJlVDFkm8ro2CGvNKSy_PGeCK4FsLxXnDpU"
    return create_client(url, key)
# def sidebar_logged_out():
