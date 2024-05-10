import streamlit as st
from PIL import Image

def main():
    st.title("Ứng dụng Đăng nhập và Đăng ký")

    # Create a sidebar with navigation options
    page = st.sidebar.radio("Chọn một tùy chọn:", ["Đăng nhập", "Đăng ký"])

    if page == "Đăng nhập":
        login()
    elif page == "Đăng ký":
        signup()

def login():
    st.subheader("Đăng nhập")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")

    col1, col2 = st.columns(2)  # Divide the layout into two columns

    with st.container():
        with col1:
            with st.container():
                if st.button("Đăng nhập", use_container_width=True):
                    # Add your login logic here
                    if username == "admin" and password == "123":
                        st.success("Đăng nhập thành công")
                        state["logged_in"] = True  # Set login state to True
                    else:
                        st.error("Tên đăng nhập hoặc mật khẩu không đúng")

        with col2:
            with st.container():
                if st.button("Đăng ký", use_container_width=True):
                    # Redirect to the signup page
                    signup()

def signup():
    st.subheader("Đăng ký")
    new_username = st.text_input("Tên đăng nhập mới")
    new_password = st.text_input("Mật khẩu mới", type="password")
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password")

    if st.button("Đăng ký"):
        # Add your signup logic here
        if new_password == confirm_password:
            st.success("Đăng ký thành công")
        else:
            st.error("Mật khẩu không khớp")

def main_app():
    st.title("Ảnh Đầu Vào và Đầu Ra")

    # Menu options for logged-in users
    menu_option = st.sidebar.radio("Chọn một tùy chọn:", ["Trang chính", "Đăng xuất"])

    if menu_option == "Trang chính":
        state = get_state()
        if state["logged_in"]:
            # Upload image
            uploaded_image = st.file_uploader("Kéo và thả một ảnh vào đây", type=["jpg", "jpeg", "png"])

            if uploaded_image is not None:
                # Display uploaded image
                image = Image.open(uploaded_image)
                st.image(image, caption="Ảnh Đầu Vào", use_column_width=True)

                # Process the image
                processed_image = process_image(image)

                # Display the processed image
                st.subheader("Kết quả")
                st.image(processed_image, caption="Kết quả", use_column_width=True)
    elif menu_option == "Đăng xuất":
        state = get_state()
        state["logged_in"] = False  # Log out the user
        st.experimental_rerun()  # Rerun the app to update UI

def process_image(image):
    # Placeholder processing: resize the image
    processed_image = image.resize((image.width // 2, image.height // 2))
    return processed_image

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Initialize login state
        
    if not st.session_state.logged_in:
        main()  # Show login page if not logged in
    else:
        main_app()  # Show main app if logged in
