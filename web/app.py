import streamlit as st
from PIL import Image, ExifTags
from datetime import datetime
from packages.encode_decode import encode_image,decode_image
from packages.request_api import analyze
import pandas as pd

def correct_orientation(image):
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = image._getexif()
    if exif is not None and orientation in exif:  # Thêm kiểm tra này
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, ewaxpand=True)
    return image

def app():
    with st.container(border=True):
        # st.title("Ảnh Đầu Vào và Đầu Ra")
        uploaded_image = st.file_uploader("Kéo và thả", type=["jpg", "jpeg", "png"])
        print(uploaded_image)

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
        
            corrected_image = correct_orientation(image)
            st.image(corrected_image, use_column_width=True)
    if st.button("Gửi",use_container_width=True):
        encoded_image = encode_image(image)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = {
            'user_info': {
                'user_name': 'user name',
                'password': 'password'
            },
            'image_info': {
                'image': encoded_image,
                'date': current_datetime 
            }
        }
        with st.container(border=True):
            results = analyze(item=item).json()
            predicted_image = decode_image(results['image_info']['predicted_image'])
            st.image(predicted_image,caption="Kết quả", use_column_width= True)

if __name__ == "__main__":
    app()