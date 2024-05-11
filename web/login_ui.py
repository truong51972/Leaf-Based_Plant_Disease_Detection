import streamlit as st
import time
from packages.request_api import check_login
from packages.request_api import create_new_user
from packages.encode_decode import encrypt_password
from packages.preprocess_text import is_valid
state = {"logged_in": False}

def login_ui():
    global state
    st.text_input("Tên đăng nhập", key= 'username')
    st.session_state['username'] = st.session_state['username'].strip()
    password = st.text_input("Mật khẩu", type="password")
    st.session_state['encrypted_password'] = encrypt_password(password).decode()
    
    if st.button("Đăng nhập", use_container_width=True):
        user_info = {
            'user_name': st.session_state.get('username'),
            'password': st.session_state.get('encrypted_password')
        }    
        response = check_login(user_info).json()
        if response['code'] == '000':
            st.success("Đăng nhập thành công!")
        elif response['code'] == '002':
            st.error("Sai mật khẩu!")
        elif response['code'] == '003':
            st.error("Tên đăng nhập không tồn tại!")
        else:
            st.error("Lỗi không xác định!")

def register_ui():
    new_username = st.text_input("Tên đăng nhập mới", key='new_username')
    new_password = st.text_input("Mật khẩu mới", type="password", key='new_password')
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key='confirm_password')
    st.session_state['encrypted_password'] = encrypt_password(new_password).decode()

    if st.button("Đăng ký"):
        if new_password == confirm_password:
            encrypted_password = encrypt_password(new_password).decode()
            user_info = {
                'user_name': st.session_state.get('new_username'),
                'password': st.session_state.get('encrypted_password')
            }
            response = create_new_user(user_info).json()
            print(response)
            if response['code'] == '000':
                st.success("Đăng ký thành công!")
            elif response['code'] == '001':
                st.error("Tên đăng nhập đẫ tồn tại!")
        else:
            st.error("Mật khẩu không khớp")


def logout():
    global state
    state["logged_in"] = False
    state["username"] = None
    st.experimental_rerun()