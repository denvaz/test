import streamlit as st
from utils import login, sidebar_logged_in, init_supabase, SessionState
import pandas as pd
import numpy as np

# Initialize Supabase client
supabase = init_supabase()

def check_serial_number(sn):
    try:
        response = supabase.table("used_sn").select("sn", "vendor").ilike("sn", "%" + sn + "%").execute()
        if len(response.data) == 0:
            subresponse = supabase.table("new_sn").select("*").ilike("sn", "%" + sn + "%").execute()
            if len(subresponse.data) == 0:
                return 'NOT FOUND', None
            else:
                return 'NOT USED', subresponse.data
        else:
            return 'USED', response.data
    except Exception as e:
        st.error(f"Error checking serial number: {e}")
        return 'ERROR', None

def display_results(sn, status, data):
    if status == 'NOT FOUND':
        st.title(f'{sn} :gray[NOT FOUND IN LISTS]')
        st.subheader("This SN is not in the [new] or [used] list.")
    elif status == 'NOT USED':
        st.title(f'{sn} :green[NOT USED]')
        df = pd.DataFrame(data, index=np.arange(1, len(data) + 1))
        st.table(df)
    elif status == 'USED':
        st.title(f'{sn} :red[USED]')
        df = pd.DataFrame(data, index=np.arange(1, len(data) + 1))
        st.table(df)

def main():
    st.set_page_config(page_title="Check SN", layout="wide")

    # Create session state object
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    if not st.session_state.session_state.logged_in:
        login()
    else:
        sidebar_logged_in()
        st.header(':gray[Check Serial number]', divider='gray')

        container = st.container()
        l, c, r = st.columns([1, 1, 1])
        with container:
            with l:
                with st.container(border=True):
                    sn = st.text_input('Serial number', '')
                    if st.button('Check', use_container_width=True):
                        with st.spinner('Checking serial number...'):
                            status, data = check_serial_number(sn)
                        display_results(sn, status, data)

if __name__ == "__main__":
    main()