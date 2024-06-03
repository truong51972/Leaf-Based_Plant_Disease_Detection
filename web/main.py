import streamlit as st
from web.login_ui import login_ui, state, register_ui, logout
from web.app import app as main_app
import time
from web.history import display_history
from web.user import user_info

def run():
    _, center, _ = st.columns([1, 8, 1])
    with center:
        with st.container():
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = False
              
            if st.session_state['logged_in']:
                tab1, tab2, tab3, tab4 = st.tabs(["Trang chủ","Thông tin cá nhân", "Lịch sử", "Đăng xuất"])
                with tab1:
                    main_app()
                with tab2:
                    user_info()
                with tab3:
                    display_history()
                with tab4:
                    if st.button("Confirm Logout"):
                        logout()
            else:
                if 'logout_success' in st.session_state and st.session_state['logout_success']:
                    st.success("Bạn đã đăng xuất thành công!")
                    time.sleep(1.6)
                    st.session_state['logout_success'] = False
                    st.rerun()
                    
                else:
                    options = ["Đăng nhập", "Đăng kí"]
                    choice = st.selectbox("Chọn 1 tùy chọn", options)
                    if choice == "Đăng nhập":
                        login_ui()
                    elif choice == "Đăng kí":
                        register_ui()

if __name__ == "__main__":
    run()
