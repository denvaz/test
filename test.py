import streamlit as st
import bcrypt

# Class for managing session state
class SessionState:
    def __init__(self):
        self.logged_in = False

# Function for checking password
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Create session state object
if 'session_state' not in st.session_state:
    st.session_state.session_state = SessionState()

# Application title
# st.title('Учет серийных номеров устройств')

if not st.session_state.session_state.logged_in:
    st.header('Вход')
    login = st.text_input('Логин')
    password = st.text_input('Пароль', type='password')
    if st.button('Войти'):
        # Check login and password (for demonstration, using dummy data)
        if login == 'admin' and password == 'password':
            st.session_state.session_state.logged_in = True
            st.success('Успешный вход!')
            st.experimental_rerun()
        else:
            st.error('Неверный логин или пароль')
else:
    st.write('Добро пожаловать! Вы успешно авторизовались.')
    
    # Add menu
    st.sidebar.header('Меню')
    if st.sidebar.button('Найти SN'):
        # Display content for "Найти SN"
        st.write('Выбран пункт меню: Найти SN')
        st.title('Найти SN')
        # Add code to search for SN here

    if st.sidebar.button('Статусы кейсов'):
        # Display content for "Статусы кейсов"
        st.write('Выбран пункт меню: Статусы кейсов')
        st.title('Статусы кейсов')
        # Add code to display case statuses here

    if st.sidebar.button('Использованные SN'):
        # Display content for "Использованные SN"
        st.write('Выбран пункт меню: Использованные SN')
        st.title('Использованные SN')
        # Add code to display used SN here

    if st.sidebar.button('Методы'):
        # Display content for "Методы"
        st.write('Выбран пункт меню: Методы')
        st.title('Методы')
        # Add code to display methods here