import streamlit as st
from web.login_ui import state
from packages.request_api import change_password
from packages.encode_decode import encrypt_password

def user_info():
    st.title("Thông tin cá nhân")

    if 'user_name' in st.session_state and st.session_state['user_name']:
        st.write(f"Xin chào, {st.session_state['user_name']}!")

    if 'show_change_password' not in st.session_state:
        st.session_state['show_change_password'] = False

    if st.button("Đổi mật khẩu"):
        st.session_state['show_change_password'] = not st.session_state['show_change_password']

    if st.session_state['show_change_password']:
        with st.form("Change Password Form"):
            current_password = st.text_input("Mật khẩu hiện tại", type="password")
            new_password = st.text_input("Mật khẩu mới", type="password")
            confirm_new_password = st.text_input("Xác nhận mật khẩu mới", type="password")
            change_password_button = st.form_submit_button("Thay đổi mật khẩu")

            if change_password_button:
                if not current_password or not new_password or not confirm_new_password:
                    st.error("Vui lòng điền đầy đủ thông tin.")
                elif new_password != confirm_new_password:
                    st.error("Mật khẩu mới và xác nhận mật khẩu không khớp.")
                else:
                    encrypted_new_password = encrypt_password(new_password).decode()

                    item = {
                        'user_info': {
                            'user_name': st.session_state.get('user_name'),
                            'password': st.session_state.get('encrypted_password')
                        },
                        'new_password': encrypted_new_password
                    }

                    response = change_password(item=item).json()

                    if response:
                        if response['code'] == '000':
                            st.success("Mật khẩu đã được thay đổi thành công!")
                            st.session_state['show_change_password'] = False
                        else:
                            st.error("Đã xảy ra lỗi khi thay đổi mật khẩu. Vui lòng thử lại sau.")
                    else:
                        st.error("Không nhận được phản hồi từ máy chủ.")
