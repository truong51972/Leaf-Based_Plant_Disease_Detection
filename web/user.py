import streamlit as st
from packages.request_api import change_password
from packages.encode_decode import encrypt_password
from datetime import datetime, timedelta
from packages.request_api import get_statistics, get_gardens_info
from packages.__request import _request
import pandas as pd
import matplotlib.pyplot as plt # type: ignore


def user_info():
    st.title("Thông tin cá nhân")

    if 'user_name' in st.session_state and st.session_state['user_name']:
        st.write(f"Xin chào, {st.session_state['user_name']}!")

    tab1, tab2 = st.tabs(["Thống kê", "Đổi mật khẩu"])

    with tab1:
        statistics_ui()

    with tab2:
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

                response = change_password(item=item, request= _request).json()

                if response:
                    if response['code'] == '000':
                        st.success("Mật khẩu đã được thay đổi thành công!")
                    else:
                        st.error("Đã xảy ra lỗi khi thay đổi mật khẩu. Vui lòng thử lại sau.")
                else:
                    st.error("Không nhận được phản hồi từ máy chủ.")

def fetch_gardens_statistics():
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }
    response = get_gardens_info(item=item, request=_request).json()
    garden_info = response.get('garden_info', {})
    garden_names = garden_info.get('Tên vườn', [])
    return garden_names

def statistics_ui():    
    st.subheader("Thống kê của bạn")

    garden_names = fetch_gardens_statistics()
    garden_name = st.selectbox("Chọn tên vườn", garden_names, key="garden_selectbox")
    
    selected_date = st.date_input("Vui lòng chọn ngày để xem thống kê.", datetime.today() - timedelta(days=1))
    end_date = st.date_input("Vui lòng chọn ngày kết thúc để xem thống kê.", datetime.today(), key="end_date")
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        },
        'start_date': selected_date_str,
        'end_date': end_date_str,
        'garden_name': garden_name,
    }

    if st.button("Xem thống kê", use_container_width=True, key="view_statistics_button"):
        response = get_statistics(item=item, request=_request).json()
        df_statistics = pd.DataFrame(response['statistic'])
        df_statistics= df_statistics.T
        st.dataframe(df_statistics)