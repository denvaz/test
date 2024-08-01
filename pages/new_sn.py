import streamlit as st
import pandas as pd
import numpy as np
from utils import login, sidebar_logged_in, init_supabase, SessionState

# Initialize Supabase client
init_supabase()


def fetch_vendor_list(supabase):
    response = supabase.table("vendor_list").select("vendor").execute()
    return [row['vendor'] for row in response.data]

def main():
    supabase = init_supabase()
    vendor_list = fetch_vendor_list(supabase)

    st.set_page_config(page_title="New SN", layout="wide")

    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    if not st.session_state.session_state.logged_in:
        login()
    else:
        sidebar_logged_in()
# PAGE CONTENT GOES HERE #################################################################
        st.header(':green[NEW] SN', divider='green')
        maincontainer = st.container(border=False)
        with maincontainer:
            col1, col2, col3 = st.columns([1, 2, 1.5])
            with col1:
                firstcontainer = st.container(border=True)
                with firstcontainer:
                    vendor = st.selectbox("Vendor", (vendor_list), placeholder="select vendor", index=None)
                    if vendor:
                        response = supabase.table("new_sn").select("vendor", "sn", "model","expiredate").filter("vendor", "eq", vendor).execute()
                        model_list = list(set(row['model'] for row in response.data))
                        model_list.append("All models")
                        model = st.selectbox("Model", (model_list), placeholder="select model", index=len(model_list) - 1)
                        if st.button("🔍 Search"):
                            if model == "All models":
                                response = supabase.table("new_sn").select("vendor", "sn", "model", "expiredate").filter("vendor", "eq", vendor).execute()
                            else:
                                response = supabase.table("new_sn").select("vendor", "sn", "model", "expiredate").filter("vendor", "eq", vendor).filter("model", "eq", model).execute()
                            df = pd.DataFrame(response.data, index=np.arange(1, len(response.data) + 1))
                            with col2:
                                seccontainer = st.container(border=True, height=600)
                                with seccontainer:
                                    st.table(df)

if __name__ == "__main__":
    main()
