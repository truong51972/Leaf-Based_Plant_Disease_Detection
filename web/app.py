import streamlit as st
from PIL import Image, ExifTags
from packages.encode_decode import encode_image
from packages.encode_decode import decode_image

def correct_orientation(image):
    try:
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
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
    return image

def app():
    st.title("Ảnh Đầu Vào và Đầu Ra")
    uploaded_image = st.file_uploader("Kéo và thả", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        # Correct orientation based on EXIF data
        corrected_image = correct_orientation(image)
        st.image(corrected_image, use_column_width=True)
        if st.button("Gửi"):
            st.write("Bức ảnh đã được gửi!")

if __name__ == "__main__":
    app()
