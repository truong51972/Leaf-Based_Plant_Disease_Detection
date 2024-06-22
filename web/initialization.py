import streamlit as st
from web.login_ui import register_ui
from packages.request_api import create_new_user
import pandas as pd

def initialization():
    tab1, tab2, tab3 = st.tabs(['Thêm vườn','Thêm nhân viên','Xem nhân viên'])
    with tab1:
        add_garden()
    with tab2:
        register_ui()
    with tab3:
        show_staff()

def add_garden():
    with st.container(border=True):
        st.subheader("Thêm vườn và luống")
        col1, col2, col3 = st.columns([0.5,0.3,0.2])
        with col1:
            gardenName = st.text_input("Tên vườn")          
        with col2:
            plantName = st.selectbox("Tên loại cây", options=['Cà chua', 'Khoai tây'])
        with col3:
            lineNum = st.number_input(f"Số luống", min_value=1, max_value=100, value=1)
        
        if st.button("Xác nhận", use_container_width=True):
            item = {
            'user_info': {
                'user_name': st.session_state.get('user_name'),
                'password': st.session_state.get('encrypted_password')
            },
            'initialization': {
                        'planName': plantName,
                        'garden_name': gardenName,
                        'line_num':lineNum
                    }
            }
def show_staff():
    item = {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    if st.button("Xem nhân viên"):
        response =  create_new_user(item=item).json()       
        df_staff = pd.DataFrame(response)
        st.dataframe = (df_staff)
    
        