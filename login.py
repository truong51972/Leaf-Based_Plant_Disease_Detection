import streamlit as st
import time

state = {"logged_in": False}

def login_ui():
    global state
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng nhập", use_container_width=True):
        if username == "admin" and password == "123":
            st.success("Chào mừng bạn quay lại, {}!".format(username))
            state["logged_in"] = True
            state["username"] = username
            time.sleep(1.8)
            st.experimental_rerun()
        else:
            st.error("Tên đăng nhập hoặc mật khẩu không đúng")

def register_ui():
    new_username = st.text_input("Tên đăng nhập mới")
    new_password = st.text_input("Mật khẩu mới", type="password")
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password")
    if st.button("Đăng ký"):
        if new_password == confirm_password:
            st.success("Đăng ký thành công")
        else:
            st.error("Mật khẩu không khớp")

def logout():
    global state
    state["logged_in"] = False
    state["username"] = None
    st.experimental_rerun()