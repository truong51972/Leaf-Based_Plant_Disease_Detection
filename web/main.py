import streamlit as st
from web.login_ui import login_ui, state, register_ui, logout
from web.app import app as main_app
from web.user import user_profile

def run():
    if state["logged_in"]:
        st.sidebar.title("Menu")
        menu_choice = st.sidebar.selectbox(" ", ["Trang chủ", "Thông tin cá nhân", "Cài đặt", "Đăng xuất"])
        if menu_choice == "Trang chủ":
            st.write("Đây là trang chủ")
        elif menu_choice == "Thông tin cá nhân":
            user_profile()
        elif menu_choice == "Cài đặt":
            st.write("Cài đặt")
        elif menu_choice == "Đăng xuất":
            logout()
            state["logged_in"] = False  # Reset logged_in state after logout
        main_app()  # Display main application when logged in
        
    else:
        _, center, _ = st.columns([1, 8, 1])
        with center:
            with st.container():
                options = ["Đăng nhập", "Đăng kí"]
                choice = st.selectbox("Chọn 1 tùy chọn", options)
                if choice == "Đăng nhập":
                    login_ui()
                elif choice == "Đăng kí":
                    register_ui()

if __name__ == "__main__":
    run()
