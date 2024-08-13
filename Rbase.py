import streamlit as st
from datetime import datetime
from utils import login, sidebar_logged_in, init_supabase, SessionState
# from streamlit_extras.stodo import to_do
# from streamlit_extras.stoggle import stoggle
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

def delete_matching_sn_records():
    # Получаем все строки из таблицы used_sn
    used_sn_data = supabase.table('used_sn').select('sn').execute()
    used_sn_list = [row['sn'] for row in used_sn_data.data]

    # Переменная для хранения количества удаленных строк
    deleted_count = 0

    # Перебираем все значения sn из таблицы used_sn
    for sn in used_sn_list:
        # Проверяем наличие строки с таким же значением sn в таблице new_sn
        new_sn_data = supabase.table('new_sn').select('sn').eq('sn', sn).execute()
        
        # Если строка найдена, удаляем ее
        if new_sn_data.data:
            supabase.table('new_sn').delete().eq('sn', sn).execute()
            deleted_count += 1

    # Выводим количество удаленных строк
    st.info(f"Количество удаленных строк: {deleted_count}")

# def example1():
#     to_do(
#         [(st.write, "☕ Take my coffee")],
#         "coffee",
#     )
#     to_do(
#         [(st.write, "🥞 Have a nice breakfast")],
#         "pancakes",
#     )
#     to_do(
#         [(st.write, ":train: Go to work!")],
#         "work",
#     )

# def example2():
#     stoggle(
#         "Click me!",
#         """🥷 Surprise! Here's some additional content""",
#     )

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

    left.button("my addresses", use_container_width=True)
    left.button("my tasks", use_container_width=True)

    # value = 
    # right.header(f'Labels: {value} / 10')
    right.progress(30)
  
  
# if st.button("CLAEN NEW SN LIST"):
#     clean_new_sn()
# if st.button("CLAEN NEW SN LIST 2"):
#     delete_matching_sn_records()

# if st.button("BUTTON1"):
# example1()
# example2()
