import streamlit as st
import time
from packages.request_api import check_login, create_new_user
from packages.encode_decode import encrypt_password
from packages.preprocess_text import is_valid

state = {"logged_in": False}

def login_ui():
    with st.form("Login Form"):
        st.session_state.user_name = st.text_input("Tên đăng nhập", key='username', help='Tên đăng nhập không được chứ khoảng trắng hoặc kí tự đặc biệt!')
        password = st.text_input("Mật khẩu", type="password", key='password')
        submit_button = st.form_submit_button("Đăng nhập")

    if submit_button:
        error_message = ""
        
        if not st.session_state.user_name.strip() or not password.strip():
            error_message += "Tên đăng nhập và mật khẩu không được để trống!\n"
        else:
            if not is_valid(st.session_state.user_name):
                error_message += "Tên đăng nhập không hợp lệ!\n"
            if not password.strip():
                error_message += "Mật khẩu không được để trống!\n"

        if error_message:
            st.error(error_message)
            return
        
        if is_valid(st.session_state.user_name) and password.strip():
            st.session_state.encrypted_password = encrypt_password(password).decode()
            user_info = {
                'user_name': st.session_state.user_name,
                'password': st.session_state.encrypted_password
            }
            response = check_login(user_info).json()
            if response['code'] == '000':
                st.success("Đăng nhập thành công!")
                st.session_state['logged_in'] = True
                time.sleep(1)
                st.rerun()
            elif response['code'] == '002':
                st.error("Sai mật khẩu!")
            elif response['code'] == '003':
                st.error("Tên đăng nhập không tồn tại!")
            elif response['code'] == '404':
                st.error("Không tìm thấy server")
            else:
                st.error("Lỗi không xác định!")
        if error_message:
            st.markdown(f"<p style='color:red'>{error_message}</p>", unsafe_allow_html=True)

def register_ui():
    with st.form("Registration Form"):
        new_username = st.text_input("Tên đăng nhập mới", key='new_username', help='Tên đăng ký không được chứ khoảng trắng hoặc kí tự đặc biệt!')
        new_password = st.text_input("Mật khẩu mới", type="password", key='new_password')
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key='confirm_password')
        submit_button = st.form_submit_button("Đăng ký")

    if submit_button:
        user_name = new_username.strip()
        error_message = ""
        
        if not user_name:
            error_message += "Tên đăng nhập không được để trống!\n"
        if not new_password.strip():
            error_message += "Mật khẩu không được để trống!\n"
        elif not is_valid(user_name):
            error_message += "Tên đăng kí không được chứa kí tự đặc biệt!\n"

        if error_message:
            st.error(error_message)
            return

        if new_password == confirm_password:
            encrypted_password = encrypt_password(new_password).decode()
            user_info = {
                'user_name': user_name,
                'password': encrypted_password
            }
            response = create_new_user(user_info).json()
            if response['code'] == '000':
                st.success("Đăng ký thành công! Vui lòng đăng nhập.")
            elif response['code'] == '001':
                st.error("Tên đăng nhập đã tồn tại!")
            elif response['code'] == '404':
                st.error("Không tìm thấy server")
        else:
            st.error("Mật khẩu không khớp")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['logout_success'] = True
    st.rerun()