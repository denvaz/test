import streamlit as st
from datetime import datetime
from utils import login, sidebar_logged_in, init_supabase, SessionState
from streamlit_extras.stodo import to_do
st.set_page_config(page_title="Amazon receipt", layout="wide")

def clean_new_sn():
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Выполняем запрос для удаления строк
    response = supabase.table('new_sn').delete().lt('expiredate', current_date).execute()

    # Проверяем результат и выводим количество удаленных строк
    if response.data:
        # `response.data` может содержать информацию о удаленных строках, если это возможно
        deleted_count = len(response.data)
        st.success(f"Строки успешно удалены. Количество удаленных строк: {deleted_count}.")
    else:
        # Проверяем наличие ошибки
        if response.error:
            st.error(f"Ошибка: {response.error}")
        else:
            st.info("Не удалось определить количество удаленных строк.")

    # Выводим количество удаленных строк
    st.info(f"Количество удаленных строк: {deleted_count}")


# Create session state object
if 'session_state' not in st.session_state:
    st.session_state.session_state = SessionState()

if not st.session_state.session_state.logged_in:
    login()
else:
    supabase = init_supabase()
    sidebar_logged_in()
# PAGE CONTENT GOES HERE #################################################################
    st.header(f'Hi :red[ {st.session_state.session_state.user}]!', divider='red')
    
    left, middle, right = st.columns([1,5,1], vertical_alignment="bottom")

    # left.button("my addresses", use_container_width=True)
    # left.button("my tasks", use_container_width=True)

    value = 3
    right.header(f'Labels: {value} / 10')
    right.progress(30)
    if st.button("Очистить список New SN"):
        clean_new_sn

    st.subheader("EXPIREMENTAL")
    to_do(
    [(st.write, "☕ Take my coffee")],
    "coffee",
    )
    to_do(
        [(st.write, "🥞 Have a nice breakfast")],
        "pancakes",
    )
    to_do(
        [(st.write, ":train: Go to work!")],
        "work",
    )