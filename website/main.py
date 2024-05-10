from login_UI import login_ui, register_ui
import streamlit as st
def run():
    _, center, _= st.columns([.15,.7,.15])
    print(1)
    with center:
        with st.container(border=True):
            options = ["Login", "Register"]
            col1, _= st.columns([.3,.7])
            with col1: 
                choice = st.selectbox("Choose an option", options)
            if choice == "Login":
                login_ui()
            elif choice == "Register":
                register_ui()

# if __name__ == "__main__":
#     main()