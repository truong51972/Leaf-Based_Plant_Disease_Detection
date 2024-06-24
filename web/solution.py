import streamlit as st
import pandas as pd
from packages.request_api import get_all_solutions

def solution_list():
    st.title("Các giải pháp cho các bệnh cây trồng")

    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }

    if st.button("Xem tất cả giải pháp"):
        try:
            response = get_all_solutions(item=item).json()

            if not response:
                st.warning("Không có dữ liệu giải pháp.")
                return

            df_solution = pd.DataFrame(response)
            st.dataframe(df_solution,hide_index=True)

        except Exception as e:
            st.error(f"Lỗi khi lấy dữ liệu giải pháp: {str(e)}")
