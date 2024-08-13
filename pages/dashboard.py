import streamlit as st
import pandas as pd
from utils import login, sidebar_logged_in, init_supabase, SessionState

supabase = init_supabase()

def fetch_address_line1(supabase, user):
    response = supabase.table("case_list").select("address_line1").filter("user", "eq", user).execute()
    return list(set([row['address_line1'] for row in response.data]))

def fetch_address_line2(supabase, user, address_line1):
    response = supabase.table("case_list").select("address_line2").filter("address_line1", "eq", address_line1).filter("user", "eq", user).execute()
    return [row['address_line2'] for row in response.data]

def fetch_vendor_list(supabase):
    response = supabase.table("vendor_list").select("vendor").execute()
    return [row['vendor'] for row in response.data]

def save_data_to_db(supabase, df, address_line1, address_line2):
    for _, row in df.iterrows():
        data = {
            "vendor": row["vendor"],
            "case_status": row["case_status"],
            "description": row["description"],
            "track_number": row["track_number"],
            "address_line1": address_line1,
            "address_line2": address_line2
        }
        response = supabase.table("case_list").insert(data).execute()
        if 'error' in response and response['error']:
            st.error(f"Error inserting data: {response.error_message}")

def build_query(supabase, user, address_line1, address_line2):
    query = supabase.table("case_list").select("vendor", "case_status", "last_update", "description", "track_number")
    if user:
        query = query.filter("user", "eq", user)
    if address_line1:
        query = query.filter("address_line1", "eq", address_line1)
    if address_line2:
        query = query.filter("address_line2", "eq", address_line2)
    return query.execute()

def case_column_config(vendor_list):
    column_config={
        "case_status": st.column_config.SelectboxColumn(
            "Case status",
            width="medium",
            default="Не начато",
            options=[
                "⚪️Не начато",
                "🟠Начато. Жду Лейбл",
                "🟣Есть лейбл. Нужен FTID",
                "🕑Едет на ремонт",
                "🟡Приехал на ремонт.",
                "🔵В работе",
                "🟢Выполнен",
                "⚫️Отказ",
            ],
            required=True,
        ),
        "vendor": st.column_config.SelectboxColumn(
            "Vendor",
            width="medium",
            options=vendor_list,
            required=True,
        ),
        "description": st.column_config.Column(
            "Description",
            width="medium",
        ),
        "track_number": st.column_config.Column(
            "Track number",
            width="medium",
        )
    }
    return column_config

def main():
    st.set_page_config(page_title="Dashboard", layout="wide")

    # Create session state object
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    if not st.session_state.session_state.logged_in:
        login()
    else:
        sidebar_logged_in()
        # PAGE CONTENT GOES HERE #################################################################
        st.header(':violet[DASHBOARD]', divider='violet')
        with st.expander("Фильтры", icon="🔽"):
            us, l1, l2, space = st.columns([0.3, 0.5, 0.3, 2])
            user = us.selectbox("Select user", ("purple", "kitkat"))
            address_line1 = l1.selectbox("Select address line 1", fetch_address_line1(supabase, user), None)
            l1state = True
            if address_line1:
                l1state = False
                
            address_line2 = l2.selectbox("Select address line 2", fetch_address_line2(supabase, user, address_line1), None, disabled=l1state)

        response = build_query(supabase, user, address_line1, address_line2)
        df = pd.DataFrame(response.data)
        vendor_list = fetch_vendor_list(supabase)
        
        if 'edited_df' not in st.session_state:
            st.session_state.edited_df = df
        add_row = st.empty()
        edited_df = st.data_editor(st.session_state.edited_df, column_config=case_column_config(vendor_list), num_rows="fixed", hide_index=True)


        # Добавление новой строки
        with add_row:
            if st.button("Add row"):
                empty_df_row = pd.DataFrame({col: '' for col in df.columns}, index=[0])
                st.session_state.edited_df = pd.concat([st.session_state.edited_df, empty_df_row], ignore_index=True)
                st.experimental_rerun()

        # Сохранение изменений
        if st.button("Save Changes"):
            save_data_to_db(supabase, edited_df, address_line1, address_line2)
            st.success("Data successfully saved!")

if __name__ == "__main__":
    main()
