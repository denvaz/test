import streamlit as st
from utils import login, sidebar_logged_in, init_supabase, SessionState
from streamlit_datalist import stDatalist
supabase = init_supabase()


def fetch_data(supabase, user, address_line1=None, address_line2=None):
    query = supabase.table("case_list").select("vendor", "case_status", "description", "track_number", "person_name")
    if user:
        query = query.filter("user_name", "eq", user)
    if address_line1:
        query = query.filter("address_line1", "eq", address_line1)
    if address_line2:
        query = query.filter("address_line2", "eq", address_line2)
    return query.execute()

def fetch_address_lines(supabase, user, address_line1=None):
    if address_line1:
        response = supabase.table("case_list").select("address_line2").filter("address_line1", "eq", address_line1).filter("user_name", "eq", user).execute()
        return [row['address_line2'] for row in response.data]
    else:
        response = supabase.table("case_list").select("address_line1").filter("user_name", "eq", user).execute()
        return list(set([row['address_line1'] for row in response.data]))

def case_column_config():
    return {
        "case_status": st.column_config.Column("Case status", width="medium", disabled=True),
        "vendor": st.column_config.Column("Vendor", width="medium", disabled=True),
        "description": st.column_config.Column("Description", width="medium", disabled=True),
        "track_number": st.column_config.Column("Track number", width="medium", disabled=True)
    }

def fetch_vendor_list(supabase):
    response = supabase.table("vendor_list").select("vendor").execute()
    return {row['vendor'] for row in response.data}

def display_cases(response, vendor_color_mapping, user, address1, address2, more):
    vendors = [row["vendor"] for row in response.data]
    person_name = list(set(row["person_name"] for row in response.data if row["person_name"] is not None))
    colors = [vendor_color_mapping.get(vendor, "gray") for vendor in vendors]
    
    # Создание гиперссылок для каждого трек-номера с корректной стилизацией и вертикальными отступами
    tags_with_links = []
    for i, row in enumerate(response.data):
        track_number = row.get("track_number")
        vendor = row.get("vendor")
        case_status = row.get("case_status")
        color = colors[i]
        

        if track_number:  # Проверка, что трек-номер существует
            if track_number.startswith("1Z"):  # UPS трек-номер
                tracking_link = f"https://www.ups.com/track?loc=en_US&tracknum={track_number}"
            elif track_number.isdigit() and len(track_number) in [12, 15]:  # FedEx трек-номер
                tracking_link = f"https://www.fedex.com/fedextrack/?tracknumbers={track_number}"
            else:
                tracking_link = None  # Если трек-номер не распознан

        if track_number:  # Проверка, что трек-номер существует
            if case_status == "⚫️Отказ" or case_status == "🟢Выполнен":
                tags_with_links.append(f'<span style="display:inline-block; background-color: black; color: grey; opacity: .9; text-decoration: none; border-radius: 0.5rem; padding: 0 10px; margin-block: 1px; margin-right: 4px;">{vendor or "Unknown Vendor"}</span>')
            else:
                tags_with_links.append(f'<a href="{tracking_link}" target="_blank" style="display:inline-block; background-color: {color}; color: #ffffff; border-radius: 0.5rem; padding: 0 10px; text-decoration: none; margin-block: 1px; margin-right: 4px;">{vendor}</a>')

        else:
            if case_status == "⚫️Отказ" or case_status == "🟢Выполнен":
                tags_with_links.append(f'<span style="display:inline-block; background-color: black; color: grey; opacity: .7; text-decoration: none; border-radius: 0.5rem; padding: 0 10px; margin-block: 1px; margin-right: 4px;">{vendor or "Unknown Vendor"}</span>')
            else: 
                tags_with_links.append(f'<span style="display:inline-block; background-color: {color}; color: #ffffff; opacity: .7; border-radius: 0.5rem; padding: 0 10px; margin-block: 1px; margin-right: 4px;">{vendor or "Unknown Vendor"}</span>')

    tags_container = (" ".join(tags_with_links))
    
    if more:
        with st.container(border=True):
            c1, c2 = st.columns([0.5, 2], vertical_alignment="top")
            with c1:
                person_name = ", ".join(person_name)
                st.write(f":white[{person_name}]")
                st.subheader(address2)
                st.markdown(tags_container, unsafe_allow_html=True)
            with c2:
                st.data_editor([row for row in response.data], column_config=case_column_config(), num_rows="fixed", hide_index=True)
                if st.button("📝Редактировать", key=user + address1 + str(address2)):
                    st.session_state.address_line1 = address1
                    st.session_state.address_line2 = address2
                    st.switch_page("pages/dashboard.py")
    else:
        
        c1, c2, c3, c4, c5 = st.columns([1.8, 1.2, 3, 1.5, 5], vertical_alignment="center", gap="small")
        st.html('<div style="border: 1px solid #0054a31a;"></div>')
        with c1:
            st.subheader(address2)
        with c2:
            person_name = ", ".join(person_name)
            st.write(f":white[{person_name}]")
            
        with c3:
            st.markdown(tags_container, unsafe_allow_html=True)
        with c4:
            if st.button("📝Редактировать", key=user + address1 + str(address2)):
                st.session_state.address_line1 = address1
                st.session_state.address_line2 = address2
                st.switch_page("pages/dashboard.py")



def save_data_to_db(supabase, user, address_line1, address_line2, person_name):
    data = {
        "user_name": user,
        "address_line1": address_line1,
        "address_line2": address_line2,
        "person_name": person_name,
        "vendor": None,
        "case_status": "⚪️Не начато",
        "description": None,
        "track_number": None,
    }
    try:
        supabase.table("case_list").insert(data).execute()
        st.success("Новый адрес успешно добавлен!")
    except Exception as e:
        st.error(f"Exception occurred: {e}")

def main():
    st.set_page_config(page_title="Method", layout="wide")

    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    if not st.session_state.session_state.logged_in:
        login()
    else:
        
        sidebar_logged_in()
        vendor_color_mapping = {
            "DELL": "#0179b7", "Acer": "#7dbc42", "Dyson": "#ed389b",
            "Yamaha": "#462076", "Corsair": "#e9e600", "Nuwave": "#e4262e"
        }

        fc1, fc2, fc3, fc4, fc5 = st.columns([1, 1, 0.1, 1.5, 6], vertical_alignment="center", gap="small")
        user = fc1.selectbox("user", ("Purple", "Kitkat"), label_visibility="collapsed")
        more = fc2.toggle("Подробнее")
        new_address = fc4.popover("Добавить адрес", use_container_width=True)
        with new_address:
            new_address_line1 = stDatalist("Addres line 1", fetch_address_lines(supabase, user))
            c1,c2 = st.columns([1,1])
            new_address_line2_prefix = c1.selectbox("Type", ["Apt", "Unit", "Suite", "Floor", "Building", "Room", "Wing", "Box", "Office", "Block", "Section", "Cell"])
            new_address_line2 = new_address_line2_prefix + " " + c2.text_input("Addres line 2", autocomplete="off")
            person_name = st.text_input("Name")
            if st.button("Сохранить"):
                response = supabase.table("case_list").select("address_line1", "address_line2", "user_name").filter('address_line1', 'eq', new_address_line1).filter('address_line2', 'eq', new_address_line2).execute()
                if len(response.data) > 0:
                    st.error("Такой адрес уже используется")
                else:
                    save_data_to_db(supabase, user, new_address_line1, new_address_line2, person_name)

        addresses1 = fetch_address_lines(supabase, user)

        for address1 in addresses1:
            st.header(f':blue[{address1}]', divider='blue')
            addresses2 = list(set(fetch_address_lines(supabase, user, address1)))
            
            for address2 in addresses2:
                response = fetch_data(supabase, user, address1, address2)
                display_cases(response, vendor_color_mapping, user, address1, address2, more)
            st.header("")

if __name__ == "__main__":
    main()
