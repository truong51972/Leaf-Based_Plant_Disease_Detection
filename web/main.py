import streamlit as st
from web.login_ui import login_ui, logout   
from web.app import app as main_app
import time
from web.history import display_history
from web.user import user_info
from web.initialization import initialization
from web.solution import solution_list
import os

DEV_MODE = os.getenv('DEV_MODE', 'False').lower() == 'true'
st.set_page_config(layout="wide")

def run():
    _, center, _ = st.columns([1, 8, 1])
    with center:
        with st.container():
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = False

            if 'is_manager' not in st.session_state:
                st.session_state['is_manager'] = False

            if 'user_name' not in st.session_state:
                st.session_state['user_name'] = ""
                
            if DEV_MODE:
                st.session_state['logged_in'] = True
                st.session_state['is_manager'] = True
                st.session_state['user_name'] = "Manager"
                st.write("Chế độ phát triển đang bật: Tự động đăng nhập.")

            if st.session_state['logged_in']:
                if st.session_state['is_manager']:
                    tabs = ["Thông tin cá nhân", "Lịch sử", "Tất cả giải pháp", "Quản lý", "Đăng xuất"]
                    tab2, tab3, tab4, tab5, tab6 = st.tabs(tabs)
                else:
                    tabs = ["Trang chủ", "Thông tin cá nhân", "Lịch sử", "Tất cả giải pháp", "Đăng xuất"]
                    tab1, tab2, tab3, tab4, tab6 = st.tabs(tabs)

                if not st.session_state['is_manager']:
                    with tab1:
                        main_app()
                with tab2:
                    user_info()
                with tab3:
                    display_history()
                with tab4:
                    solution_list()

                if st.session_state['is_manager']:
                    with tab5:
                        initialization()

                with tab6:
                    if st.button("Xác nhận đăng xuất"):
                        logout()
                        st.session_state['logged_in'] = False
                        st.session_state['logout_success'] = True
                        st.experimental_rerun()
            else:
                if 'logout_success' in st.session_state and st.session_state['logout_success']:
                    st.success("Bạn đã đăng xuất thành công!")
                    time.sleep(1.6)
                    st.session_state['logout_success'] = False
                    st.experimental_rerun()
                else:
                    login_ui()

if __name__ == "__main__":
    run()
