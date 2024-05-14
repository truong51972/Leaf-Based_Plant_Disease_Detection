import streamlit as st
from web.login_ui import login_ui, state, register_ui, logout
from web.app import app as main_app
import time
from web.user import user_profile

def run():
    _, center, _ = st.columns([1, 8, 1])
    with center:
        with st.container():
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = False
            
            if st.session_state['logged_in']:
                tab1, tab2, tab3 = st.tabs(["Home", "User Profile", "Logout"])
            
                with tab1:
                    main_app()
                with tab2:
                    st.header('user_profile')
                with tab3:
                    if st.button("Confirm Logout"):
                        logout()
            else:
                if 'logout_success' in st.session_state and st.session_state['logout_success']:
                    st.success("Bạn đã đăng xuất thành công!")
                    time.sleep(2)
                    st.session_state['logout_success'] = False
                    st.experimental_rerun()
                else:
                    options = ["Đăng nhập", "Đăng kí"]
                    choice = st.selectbox("Chọn 1 tùy chọn", options)
                    if choice == "Đăng nhập":
                        login_ui()
                    elif choice == "Đăng kí":
                        register_ui()

if __name__ == "__main__":
    run()
