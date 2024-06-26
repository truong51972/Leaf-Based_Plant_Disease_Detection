import streamlit as st
from web.login_ui import register_ui, delete_employees
from packages.request_api import get_gardens_info, add_garden, get_employee_info, delete_garden
import pandas as pd


def initialization():
    tab1, tab2 = st.tabs(['Vườn','Nhân viên'])
    with tab1:
        with st.expander("Thông tin các vườn"):
            show_gardens()
        with st.expander("Thêm vườn và luống"):
            add_gardens()
        with st.expander("Xóa vườn"):
            delete_gardens()
            
    with tab2:
        with st.expander("Xem thông tin nhân viên"):
            show_employees()
        with st.expander('Thêm nhân viên'):
            register_ui()
        with st.expander("Xóa nhân viên"):
            delete_employees()
            
        
def add_gardens():
    st.subheader("Thêm vườn và luống")
    col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
    
    with col1:
        gardenName = st.text_input("Tên vườn",help='Tên vườn không được chứa khoảng trắng hoặc kí tự đặc biệt!')
    
    with col2:
        plantName = st.selectbox("Tên loại cây", options=['Cà chua', 'Khoai tây'])
    
    with col3:
        lineNum = int(st.number_input("Số luống", min_value=1, max_value=100, value=1, step=1, format="%d"))
    
    if st.button("Xác nhận", use_container_width=True):
        if not gardenName:
            st.error("Vui lòng nhập tên vườn!")
            return
        
        item = {
            'user_info': {
                'user_name': st.session_state.get('user_name'),
                'password': st.session_state.get('encrypted_password')
            },
            'garden_info': {
                'plant_name': plantName,
                'garden_name': gardenName,
                'num_of_line': lineNum
            }
        }
        
        response = add_garden(item=item).json()
        
        if response['code'] == '000':
            st.success("Thêm vườn thành công!")
        elif response['code'] == '001':
            st.error("Thêm vườn thất bại - tên vườn đã tồn tại!")
        elif response['code'] == '404':
            st.error("Không tìm thấy server")
        else:
            st.error("Lỗi không xác định!")

def show_gardens():
    st.subheader("Thông tin các vườn")
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }
    if st.button("Lấy thông tin vườn", use_container_width=True):
        response = get_gardens_info(item=item).json()
        garden_info = response['garden_info']
        df_gardens = pd.DataFrame(garden_info)
        st.dataframe(df_gardens,hide_index=True)

def delete_gardens():
    st.subheader("Xóa vườn")
    gardenName = st.text_input("Tên vườn cần xóa")

    if st.button("Xác nhận xóa"):

        if not gardenName:
            st.error("Vui lòng nhập tên vườn cần xóa!")
            return
        
        item = {
            'user_info': {
                'user_name': st.session_state.get('user_name'),
                'password': st.session_state.get('encrypted_password')
            },
            'garden_name': gardenName
        }
        response = delete_garden(item=item).json()
        if response['code'] == '000':
            st.success("Xóa vườn thành công!")
        elif response['code'] == '001':
            st.error("Xóa vườn thất bại")
        elif response['code'] == '404':
            st.error("Không tìm thấy server")
        else:
            st.error("Lỗi không xác định!") 


def show_employees():
    item = {
        'user_name': st.session_state.get('user_name'),
        'password': st.session_state.get('encrypted_password')
    }
    if st.button("Xem bảng thông tin nhân viên", use_container_width= True):
        response = get_employee_info(item=item).json()
        employee_info = response['employee_info']
        df_employees = pd.DataFrame(employee_info)
        st.dataframe(df_employees,hide_index=True)





    
        