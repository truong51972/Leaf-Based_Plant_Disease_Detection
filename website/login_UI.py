import streamlit as st

def login_ui():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "123":
            st.success("Logged in as {}".format(username))
        else:
            st.error("Invalid username or password")

def register_ui():
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if new_password != confirm_password:
        st.warning("Passwords do not match")
    elif st.button("Register"):
        # Here you would typically handle registration logic
        st.success("Successfully registered as {}".format(new_username))

