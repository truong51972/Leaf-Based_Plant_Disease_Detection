import streamlit as st
state = {"logged_in": False}
def login_ui():
    global state
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng nhập", use_container_width=True):
        if username == "admin" and password == "123":
            st.success("Đăng nhập thành công")
            state["logged_in"] = True 
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

