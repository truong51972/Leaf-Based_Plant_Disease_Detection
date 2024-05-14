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
        error_message = ""
        
        if not user_name.strip() and not password.strip():
            error_message += "Tên đăng nhập và mật khẩu không được để trống!\n"
        else:
            if not is_valid(user_name):
                error_message += "Tên đăng nhập không hợp lệ!\n"
            
            if not password.strip():
                error_message += "Mật khẩu không được để trống!\n"
            
            if not is_valid(user_name) and not password.strip():
                error_message = "Tên đăng nhập không hợp lệ và mật khẩu không được để trống!\n"

        if is_valid(user_name) and password.strip():
            st.session_state['encrypted_password'] = encrypt_password(password).decode()
            user_info = {
                'user_name': user_name,
                'password': st.session_state.get('encrypted_password')
            }    
            response = check_login(user_info).json()
            if response['code'] == '000':
                st.success("Đăng nhập thành công!")
                time.sleep(1.8)
                st.session_state['logged_in'] = True
                st.experimental_rerun()
            elif response['code'] == '002':
                st.error("Sai mật khẩu!")
            elif response['code'] == '003':
                st.error("Tên đăng nhập không tồn tại!")
            elif response['code'] == '004':
                    st.error("Không tìm thấy sever")
            else:
                st.error("Lỗi không xác định!")

        if error_message:
            st.markdown(f"<p style='color:red'>{error_message}</p>", unsafe_allow_html=True)

def register_ui():
    new_username = st.text_input("Tên đăng nhập mới", key='new_username', help='Tên đăng ký không được chứ khoảng trắng hoặc kí tự đặc biệt!\n')
    new_password = st.text_input("Mật khẩu mới", type="password", key='new_password')
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key='confirm_password')
    st.session_state['encrypted_password'] = encrypt_password(new_password).decode()

    if st.button("Đăng ký"):
        user_name = st.session_state.get('new_username', '').strip()  
        error_message = ""
        
        if not user_name:
            error_message += "Tên đăng nhập không được để trống!\n"
        if not new_password.strip():
            error_message += "Mật khẩu không được để trống!\n"
        elif not is_valid(user_name):
            error_message += "Tên đăng kí không được chứa kí tự đặc biệt!\n"
        
        if error_message:
            st.error(error_message)
        else:
            if new_password == confirm_password:
                encrypted_password = encrypt_password(new_password).decode()
                user_info = {
                    'user_name': user_name,
                    'password': st.session_state.get('encrypted_password')
                }
                response = create_new_user(user_info).json()
                if response['code'] == '000':
                    st.success("Đăng ký thành công!")
                elif response['code'] == '001':
                    st.error("Tên đăng nhập đã tồn tại!")
                elif response['code'] == '004':
                    st.error("Không tìm thấy sever")
            else:
                st.error("Mật khẩu không khớp")




def logout():
    st.session_state['logged_in'] = False
    st.session_state['logout_success'] = True
    st.experimental_rerun()