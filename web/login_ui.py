import streamlit as st
import time
import os
from packages.request_api import check_login, add_employee, delete_employee, _request
from packages.encode_decode import encrypt_password
from packages.preprocess_text import is_valid   

DEV_MODE = os.getenv('DEV_MODE', 'False').lower() == 'true'

state = {"logged_in": False}

def login_ui(request = _request):
    st.title("Đăng nhập")
    with st.form("Login Form"):
        st.session_state.user_name = st.text_input("Tên đăng nhập", key='username', help='Tên đăng nhập không được chứa khoảng trắng hoặc kí tự đặc biệt!')
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
            if DEV_MODE:
                st.session_state['logged_in'] = True
                st.success("Đăng nhập thành công (Dev Mode)!")
                st.experimental_rerun()
            else:
                st.session_state.encrypted_password = encrypt_password(password).decode()
                user_info = {
                    'user_name': st.session_state.user_name,
                    'password': st.session_state.encrypted_password
                }

                response = check_login(user_info).json()
                if response['code'] == '000':
                    st.success("Đăng nhập thành công!")
                    time.sleep(1.3)
                    st.session_state['logged_in'] = True
                    st.session_state['is_manager'] = response.get('is_manager', False)
                    print(f"Logged in as: {st.session_state.user_name}, is_manager: {st.session_state['is_manager']}")
                    st.experimental_rerun()
                elif response['code'] == '002':
                    st.error("Sai mật khẩu!")
                elif response['code'] == '003':
                    st.error("Tên đăng nhập không tồn tại!")
                elif response['code'] == '404':
                    st.error("Không tìm thấy server")
                else:
                    st.error("Lỗi không xác định!")

def register_ui():
    with st.form("Registration Form"):
        new_username = st.text_input("Tên đăng nhập mới", key='new_username', help='Tên đăng ký không được chứa khoảng trắng hoặc kí tự đặc biệt!')
        new_password = st.text_input("Mật khẩu mới", type="password", key='new_password')
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key='confirm_password')
        submit_button = st.form_submit_button("Đăng ký")

    if submit_button:
        st.session_state.new_user_name = new_username.strip()
        error_message = ""
        
        if not st.session_state.new_user_name:
            error_message += "Tên đăng nhập không được để trống!\n"
        if not new_password.strip():
            error_message += "Mật khẩu không được để trống!\n"
        elif not is_valid(st.session_state.new_user_name):
            error_message += "Tên đăng kí không được chứa kí tự đặc biệt!\n"

        if error_message:
            st.error(error_message)
            return

        if new_password == confirm_password:
            st.session_state.new_encrypted_password = encrypt_password(new_password).decode()
            item = {
                'manager_info':{
                    'user_name': st.session_state.user_name,
                    'password': st.session_state.encrypted_password
                },
                "employee_info" : {
                    'user_name' : st.session_state.new_user_name,
                    'password' : st.session_state.new_encrypted_password
                }
            }
            response = add_employee(item=item).json()
            if response['code'] == '000':
                st.success("Đăng ký thành công! Vui lòng đăng nhập.")
            elif response['code'] == '001':
                st.error("Tên đăng nhập đã tồn tại!")
            elif response['code'] == '404':
                st.error("Không tìm thấy server")
        else:
            st.error("Mật khẩu không khớp")

def delete_employees():
    st.subheader("Xóa nhân viên")
    user_name = st.text_input("Tên nhân viên cần xóa", key='delete_username', help='Tên đăng nhập của nhân viên cần xóa')

    if st.button("Xác nhận xóa nhân viên"):
        if not user_name.strip():
            st.error("Vui lòng nhập tên nhân viên cần xóa!")
            return

        item = {
            'manager_info': {
                'user_name': st.session_state.get('user_name'),
                'password': st.session_state.get('encrypted_password')
            },
            'employee_info': {
                'user_name': user_name.strip(),
                'password': st.session_state.get('new_encrypted_password', '')
            }
        }

        response = delete_employee(item=item).json()
        if response['code'] == '000':
            st.success("Xóa nhân viên thành công!")
        elif response['code'] == '001':
            st.error("Xóa nhân viên thất bại!")
        elif response['code'] == '404':
            st.error("Không tìm thấy server")
        else:
            st.error("Tên nhân viên không tồn tại")

def logout():
    st.session_state['logged_in'] = False
    st.experimental_rerun()

if __name__ == "__main__":
    login_ui()
