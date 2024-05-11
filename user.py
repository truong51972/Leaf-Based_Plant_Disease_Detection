import streamlit as st
from login import state
def user_profile():
    st.title("Thông tin cá nhân")
    st.write(f"Xin chào, {state['username']}!")
    st.write("Dưới đây là thông tin cá nhân của bạn:")
    st.write("- Họ và tên: John Doe")
    st.write("- Email: john.doe@example.com")
    st.write("- Số điện thoại: 0123456789")