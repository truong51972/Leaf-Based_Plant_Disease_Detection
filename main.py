from login_UI import login_ui, register_ui
from process_app import app
import streamlit as st

def main():
    _, center, _= st.columns([.15,.7,.15])
    with center:
        with st.scontainer(border=True):
            options = ["Login", "Register"]
            col1, _= st.columns([.3,.7])
            with col1: 
                choice = st.selectbox("Choose an option", options)
            if choice == "Login":
                login_ui()
            elif choice == "Register":
                register_ui()

if __name__ == "__main__":
    main()