import streamlit as st
from PIL import Image

def app():
    st.title("Ảnh Đầu Vào và Đầu Ra")

    # Upload image
    uploaded_image = st.file_uploader("Kéo và thả", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Ảnh Đầu Vào", use_column_width=True)
