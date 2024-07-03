import streamlit as st
import pandas as pd
from packages.__request import _request
from packages.request_api import get_location_assignment_table, assign_employee_location

@st.cache_data
def fetch_location_assignment_table(garden_name):
    item = {
        'user_info': {
            'user_name' : st.session_state.get('user_name'),
            'password' : st.session_state.get('encrypted_password')
        },
        'garden_name': garden_name        
    }       
    result = get_location_assignment_table(item=item, request=_request).json()
    table = result['table']
    df = pd.DataFrame(table)
    print(df)
    return df.to_dict()

def assign_employees_task():
    st.subheader("Phân công")
    garden_name = st.text_input("Nhập tên vườn")
    if st.button("Bảng phân công", use_container_width=True):
        table_dict = fetch_location_assignment_table(garden_name)

        if table_dict:
            st.data_editor(
                pd.DataFrame.from_dict(table_dict),
                column_config={
                    'Tên Nhân Viên': 'Tên Nhân Viên',
                    **{f'Hàng {i+1}': f'Hàng {i+1}' for i in range(len(table_dict) - 1)}
                }
            )

# def assign_employees_task():
#     st.subheader("Phân công")
#     garden_name = st.text_input("Nhập tên vườn")
    
#     if 'table_displayed' not in st.session_state:
#         st.session_state.table_displayed = False

#     if 'table_df' not in st.session_state:
#         st.session_state.table_df = None

#     item = {
#         'user_info': {
#             'user_name' : st.session_state.get('user_name'),
#             'password' : st.session_state.get('encrypted_password')
#         },
#         'garden_name': garden_name        
#     }
    
#     if st.button("Bảng phân công", key="display_table_button", use_container_width=True):
#         if st.session_state.table_df is None:
#             result = get_location_assignment_table(item=item, request=requests).json()
#             print("Received data:", result)
#             table = result['table'])
#             st.session_state.table_df = pd.DataFrame(table)
#         st.session_state.table_displayed = True

#     if st.session_state.table_displayed and st.session_state.table_df is not None:
#         st.data_editor(
#             st.session_state.table_df,
#             column_config={
#                 'Tên Nhân Viên': 'Tên Nhân Viên',
#                 **{f'Hàng {i+1}': f'Hàng {i+1}' for i in range(len(st.session_state.table_df.columns) - 1)}
#             }
#         )
        
#         if st.button("Gửi phân công", key="assign_button"):
#             table_dict = st.session_state.table_df.to_dict(orient='list')
#             item['table'] = table_dict
            
#             response = assign_employee_location(item=item, request=requests)
#             if response.status_code == 200:
#                 data = response.json()
#                 print("Response from server:", data)
                
#                 if data['code'] == '000':
#                     st.success("Phân công đã được gửi")
#                 elif data['code'] == '003':
#                     st.warning("Không tìm thấy nhân viên")
#                 elif data['code'] == '101':
#                     st.warning("Lỗi: Đã thêm nhân viên vào vị trí hiện tại!")
#                 else:
#                     st.error("Lỗi không xác định từ server")
#             else:
#                 st.error("Lỗi khi gửi yêu cầu đến server")