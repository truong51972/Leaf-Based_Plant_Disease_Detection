import streamlit as st
from packages.request_api import change_password
from packages.encode_decode import encrypt_password
from datetime import datetime, timedelta
from packages.request_api import get_statistics
from packages.__request import _request
import pandas as pd
import matplotlib.pyplot as plt


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

def get_statistics_data(item):
    try:
        response = get_statistics(item=item, request=_request).json()
        df_statistics = pd.DataFrame(response)
        return df_statistics
    except Exception as e:
        st.error(f"Lỗi khi lấy dữ liệu thống kê")
        return pd.DataFrame() 
    
def plot_bar_chart(df_statistics, container):
    try:
        if not df_statistics.empty:
 
            filtered_df = df_statistics[df_statistics.iloc[:, 0] != 0]
            if not filtered_df.empty:

                filtered_df.iloc[:, 0] = filtered_df.iloc[:, 0].astype(int)

                labels = filtered_df.index
                values = filtered_df.iloc[:, 0].values

                colors = ['blue', 'green', 'red', 'purple', 'orange', 
                          'brown', 'pink', 'gray', 'cyan', 'yellow']

                fig, ax = plt.subplots(figsize=(15, 10))
                bars = ax.bar(labels, values, color=colors)


                ax.set_xlabel('Nhóm')
                ax.set_ylabel('Số lượng')
                ax.set_title('Biểu đồ thống kê theo nhóm', pad=20) 

                for bar in bars:
                    yval = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 1), ha='center', va='bottom')

                fig.tight_layout()
                with container:
                    st.pyplot(fig)
            else:
                st.warning("Không có dữ liệu để hiển thị biểu đồ.")
        else:
            st.warning("Không có dữ liệu để hiển thị biểu đồ.")
    except Exception as e:
        st.error(f"Lỗi khi vẽ biểu đồ: {str(e)}")

def plot_pie_chart(df_statistics, container):
    try:
        if not df_statistics.empty:
            df_statistics.iloc[:, 0] = df_statistics.iloc[:, 0].astype(int)

            labels = df_statistics.index
            values = df_statistics.iloc[:, 0].values

            colors = ['blue', 'green', 'red', 'purple', 'orange', 
                      'brown', 'pink', 'gray', 'cyan', 'yellow']

            non_zero_indices = values != 0
            labels = labels[non_zero_indices]
            values = values[non_zero_indices]

            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(values, labels=labels, colors=colors, autopct='%1.0f%%', startangle=140)

            ax.set_title('Biểu đồ phân bổ thống kê',pad=1) 
            with container:
                st.pyplot(fig)
    except Exception as e:
        st.error(f"Lỗi khi vẽ biểu đồ phân bổ: {str(e)}")

def statistics_ui():
    st.subheader("Thống kê của bạn")
    selected_date = st.date_input("Vui lòng chọn ngày để xem thống kê.", datetime.today() - timedelta(days=1))
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        },
        'date': selected_date_str,
        'garden_num': int,
        'line_num': int
    }

    if st.button("Xem thống kê"):
        df_statistics = get_statistics_data(item)
        if not df_statistics.empty:
            with st.container(border=True):
                st.write("Bảng thống kê:")
                st.dataframe(df_statistics)
        
        container1 = st.container(border=True)
        container2 = st.container(border=True)

        plot_bar_chart(df_statistics,container1)
        plot_pie_chart(df_statistics,container2)