import streamlit as st
from PIL import Image

def app():
    st.title("Ảnh Đầu Vào và Đầu Ra")
    uploaded_image = st.file_uploader("Kéo và thả", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, use_column_width=True)