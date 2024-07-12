import streamlit as st
import pandas as pd
from packages.request_api import get_all_solutions
from packages.__request import _request

def solution_list():
    st.title("Các giải pháp cho các bệnh cây trồng")

    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }

    tab1, tab2 = st.tabs(["Giải pháp cho cà chua", "Giải pháp cho khoai tây"])

    with tab1:
        st.subheader("Giải pháp cho cà chua")
        try:
            response = get_all_solutions(item=item, request=_request).json()

            if not response or 'Cà chua' not in response:
                st.warning("Không có dữ liệu giải pháp cho cà chua.")
                return

            df_solution = pd.DataFrame(response['Cà chua'])
            st.dataframe(df_solution, hide_index=True)

        except Exception as e:
            st.error(f"Lỗi khi lấy dữ liệu giải pháp cho cà chua: {str(e)}")

    with tab2:
        st.subheader("Giải pháp cho khoai tây")
        try:
            response = get_all_solutions(item=item, request=_request).json()

            if not response or 'Khoai tây' not in response:
                st.warning("Không có dữ liệu giải pháp cho khoai tây.")
                return

            df_solution = pd.DataFrame(response['Khoai tây'])
            st.dataframe(df_solution, hide_index=True)

        except Exception as e:
            st.error(f"Lỗi khi lấy dữ liệu giải pháp cho khoai tây: {str(e)}")

