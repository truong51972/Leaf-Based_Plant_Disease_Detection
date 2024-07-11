import streamlit as st
import pandas as pd
from packages.__request import _request
from packages.request_api import get_location_assignment_table, assign_employee_location, get_gardens_info

def fetch_gardens_admin():
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

def assign_employees_task():
    st.subheader("Phân công")
    
    garden_names = fetch_gardens_admin()
    garden_name = st.selectbox("Chọn tên vườn", garden_names)

    if 'table_df' not in st.session_state:
        st.session_state.table_df = None

    if 'current_garden_name' not in st.session_state:
        st.session_state.current_garden_name = ""

    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        },
        'garden_name': garden_name        
    }
    
    if garden_name != st.session_state.current_garden_name:
        st.session_state.table_df = None
        st.session_state.current_garden_name = garden_name

    if st.session_state.table_df is None:
        result = get_location_assignment_table(item=item, request=_request).json()
        
        if 'table' in result:
            table = result['table']
            st.session_state.table_df = pd.DataFrame(table)
        else:
            st.session_state.table_df = pd.DataFrame()

    table_df = st.session_state.table_df.copy()
    
    edited_table_df = st.data_editor(
        table_df,
        column_config={
            'Tên Nhân Viên': 'Tên Nhân Viên',
            **{f'Hàng {i+1}': f'Hàng {i+1}' for i in range(len(table_df.columns) - 1)},
        },
        key='data_editor'
    )

    if st.button("Gửi phân công", key="assign_button"):
        st.session_state.table_df = edited_table_df
        table_dict = edited_table_df.to_dict(orient='list')
        print(table_dict)
        item['table'] = table_dict
        
        response = assign_employee_location(item=item, request=_request)
        if response.status_code == 200:
            data = response.json()
            print("Response from server:", data)
            if data['code'] == '000':
                st.success("Phân công đã được gửi")
            elif data['code'] == '003':
                st.warning("Không tìm thấy nhân viên")
            elif data['code'] == '101':
                st.warning("Lỗi: Đã thêm nhân viên vào vị trí hiện tại!")
            else:
                st.error("Lỗi không xác định từ server")
        else:
            st.error("Lỗi khi gửi yêu cầu đến server")


