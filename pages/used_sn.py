import streamlit as st
import pandas as pd
import numpy as np
from utils import hide_sidebar_page, login, sidebar_logged_in, init_supabase, SessionState

# Initialize Supabase client
init_supabase()

def fetch_vendor_list(supabase):
    response = supabase.table("vendor_list").select("vendor").execute()
    return [row['vendor'] for row in response.data]

def main():
    supabase = init_supabase()
    vendor_list = fetch_vendor_list(supabase)

    st.set_page_config(page_title="Used SN", layout="wide")

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
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
        st.header(':red[USED] SN', divider='red')
        # Track the selected button in session state
        if 'selected_button' not in st.session_state:
            st.session_state.selected_button = 'Add SN'

        container = st.container()
        with container:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("🔍 Search", use_container_width=True):
                    st.session_state.selected_button = 'Search SN'
                if st.button("➕ Insert", use_container_width=True):
                    st.session_state.selected_button = 'Add SN'
                if st.button("📖 SN List", use_container_width=True):
                    st.session_state.selected_button = 'SN List'

            with col2:  # Place the form in the middle column
                if st.session_state.selected_button == 'Add SN':
                    with st.container(border=True):
                        vendor_list.append('➕➕➕ADD NEW VENDOR➕➕➕')
                        vendor = st.selectbox("Vendor", (vendor_list), placeholder="select vendor", index=None, label_visibility='collapsed')
                        if vendor == "➕➕➕ADD NEW VENDOR➕➕➕":
                            newvendor = st.text_input("Name of new vendor", placeholder="Name of new vendor")
                            
                        sn = st.text_input("SN", placeholder="SN", label_visibility='hidden')
                        reasoncontainer = st.container()
                        with reasoncontainer:
                            rcol1, rcol2, rcol3 = st.columns([1.5, 1, 1], gap="large")  # Adjust the column widths as needed
                            with rcol1:
                                reason = st.radio("Reason", [":green[I Used it]", ":red[Already registered]", ":grey[Other]"], horizontal=True)
                                if reason == ":green[I Used it]":
                                    reason = "used"
                                if reason == ":red[Already registered]":
                                    reason = "registered"
                                if reason == ":grey[Other]":
                                    reason = st.text_input("Describe the reason")
                       
                        submitted = st.button("➕ Add")
                        if submitted:
                            if sn == "":
                                st.error("Please fill all the required fields.")
                            else:
                                vendoradded_flag = False
                                # Check if the combination of vendor and SN already exists in the database
                                if vendor == "➕➕➕ADD NEW VENDOR➕➕➕":
                                    vendor = newvendor
                                    response = supabase.table("vendor_list").select("vendor").filter("vendor", "eq", vendor).execute()
                                    if response.data and len(response.data) > 0:
                                        st.error(f"{vendor} already exists.")
                                    else:
                                        # Insert the data into Supabase
                                        insert_data = {"vendor": vendor}
                                        response = supabase.table("vendor_list").insert(insert_data).execute()

                                        if 'error' in response and response['error']:
                                            st.error("Failed to add new vendor: " + response['error']['message'])
                                        else:
                                            st.success(f"**{vendor}** added successfully.")
                                            vendoradded_flag = True
                                response = supabase.table("used_sn").select("sn").filter("vendor", "eq", vendor).filter("sn", "eq", sn).execute()
                                if response.data and len(response.data) > 0:
                                    st.error(f"SN already exists for this vendor. {vendor}")
                                else:
                                    # Insert the data into Supabase
                                    insert_data = {
                                        "vendor": vendor,
                                        "sn": sn,
                                        "reason": reason
                                    }
                                    response = supabase.table("used_sn").insert(insert_data).execute()

                                    if 'error' in response and response['error']:
                                        st.error("Failed to add SN: " + response['error']['message'])
                                    else:
                                        if vendoradded_flag:
                                            st.success(f"**{sn}** added successfully to **{newvendor}**.")
                                            st.experimental_rerun()
                                        else:
                                            st.success(f"**{sn}** added successfully to **{vendor}**.")


                elif st.session_state.selected_button == 'SN List':
                    # Display the selectbox
                    vendor = st.selectbox("Vendor", vendor_list)

                    # Fetch data from Supabase
                    response = supabase.table("used_sn").select("sn","reason").filter("vendor", "eq", vendor).execute()
                    df = pd.DataFrame(response.data, index=np.arange(1, len(response.data) + 1))
                    st.table(df)

                elif st.session_state.selected_button == 'Search SN':
                    with st.form("search_form"):
                        sn = st.text_input("Search SN", placeholder="Search by SN", label_visibility='collapsed')
                        submitted = st.form_submit_button("🔍 Search",)
                        if submitted:
                            if sn == "":
                                st.error("Please enter a SN.")
                            else:
                                # Fetch data from Supabase
                                response = supabase.table("used_sn").select("sn","vendor","reason").ilike("sn", "%" + sn + "%").execute()
                                if len(response.data) == 0:
                                    st.error("No SN found.")
                                else:
                                    df = pd.DataFrame(response.data, index=np.arange(1, len(response.data) + 1))
                                    st.table(df)

if __name__ == "__main__":
    main()