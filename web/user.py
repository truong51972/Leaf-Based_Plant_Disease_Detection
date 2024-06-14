import streamlit as st
from packages.request_api import change_password
from packages.encode_decode import encrypt_password
from datetime import datetime, timedelta
from web.history import get_first_upload_date
from packages.request_api import statistics
import pandas as pd


def user_info():
    st.title("Thông tin cá nhân")

    if 'user_name' in st.session_state and st.session_state['user_name']:
        st.write(f"Xin chào, {st.session_state['user_name']}!")

    selected_option = st.selectbox("Chọn chức năng", ["", "Xem thống kê", "Đổi mật khẩu"])

    if selected_option == "Xem thống kê":
        statistics_ui()

    elif selected_option == "Đổi mật khẩu":
        change_password_ui()

def change_password_ui():
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
                    else:
                        st.error("Đã xảy ra lỗi khi thay đổi mật khẩu. Vui lòng thử lại sau.")
                else:
                    st.error("Không nhận được phản hồi từ máy chủ.")

def statistics_ui():
    st.subheader("Thống kê của bạn") 

    with st.container(border=True):
        first_upload_date = get_first_upload_date()
        if first_upload_date:
            st.write(f"Ngày đầu tiên gửi ảnh vào ứng dụng: {first_upload_date}")
        else:
            st.warning("Không có dữ liệu để hiển thị.")

    st.date_input("Vui lòng chọn ngày để xem thống kê.", datetime.today() - timedelta(days=1))
    item = {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    if st.button("Xem thống kê"):
        response =  statistics(item=item).json()
        if 'statistics' in response:
            df_statistics = pd.DataFrame(response['statistics'])
            df_statistics = df_statistics[['Tên bệnh',]]
            st.dataframe(df_statistics)
        else:
            st.warning("Không có dữ liệu thống kê để hiển thị.")