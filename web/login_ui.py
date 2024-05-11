import streamlit as st
import time
from packages.request_api import check_login
from packages.request_api import create_new_user
from packages.encode_decode import encrypt_password
from packages.preprocess_text import is_valid
state = {"logged_in": False}

def login_ui():
    global state
    st.text_input("Tên đăng nhập", key= 'username', help= 'Tên đăng nhập không được chứ khoảng trắng hoặc kí tự đặc biệt!')
    password = st.text_input("Mật khẩu", type="password")
    st.session_state['encrypted_password'] = encrypt_password(password).decode()
    
    if st.button("Đăng nhập", use_container_width=True):
        user_name = st.session_state.get('username').strip()
        if is_valid(user_name):
            user_info = {
                'user_name': user_name,
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
        else:
            st.error("Tên không hợp lệ!")

def register_ui():
    new_username = st.text_input("Tên đăng nhập mới", key='new_username',help= 'Tên đăng kí không được chứ khoảng trắng hoặc kí tự đặc biệt!')
    new_password = st.text_input("Mật khẩu mới", type="password", key='new_password')
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key='confirm_password')
    st.session_state['encrypted_password'] = encrypt_password(new_password).decode()

    if st.button("Đăng ký"):
        if is_valid(new_username):
            if new_password == confirm_password:
                encrypted_password = encrypt_password(new_password).decode()
                user_info = {
                    'user_name': st.session_state.get('new_username'),
                    'password': st.session_state.get('encrypted_password')
                }
                response = create_new_user(user_info).json()
                if response['code'] == '000':
                    st.success("Đăng ký thành công!")
                elif response['code'] == '001':
                    st.error("Tên đăng nhập đẫ tồn tại!")
            else:
                st.error("Mật khẩu không khớp")
        else:
            st.error("Tên không hợp lệ!")


def logout():
    global state
    state["logged_in"] = False
    state["username"] = None
    st.experimental_rerun()