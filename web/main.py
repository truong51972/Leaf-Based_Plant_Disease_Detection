import streamlit as st
from web.login_ui import login_ui, register_ui, logout
from web.app import app as main_app
import time
from web.history import display_history
from web.user import user_info
from web.test import test
import os

DEV_MODE = os.getenv('DEV_MODE', 'False').lower() == 'true'

def run():
    _, center, _ = st.columns([1, 8, 1])
    with center:
        with st.container():
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = False
            
            if DEV_MODE:
                st.session_state['logged_in'] = True
                st.write("Chế độ phát triển đang bật: Tự động đăng nhập.")

            if st.session_state['logged_in']:
                tab1, tab2, tab3, tab4,tab5 = st.tabs(["Trang chủ", "Thông tin cá nhân", "Lịch sử", "Đăng kí", "Đăng xuất"])
                with tab1:
                    test()
                with tab2:
                    user_info()
                with tab3:
                    display_history()
                with tab4:
                    register_ui()
                with tab5:
                    if st.button("Confirm Logout"):
                        logout()
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
