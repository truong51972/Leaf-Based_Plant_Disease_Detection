import streamlit as st
from PIL import Image, ExifTags
from datetime import datetime
from packages.encode_decode import encode_image, decode_image
from packages.request_api import analyze
import pandas as pd

def correct_orientation_and_resize(image, max_size=(224, 224)):
    # Handle orientation
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = image._getexif()
    if exif is not None and orientation in exif:
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    
    image = image.resize(max_size, Image.Resampling.LANCZOS)
    return image

def app():
    st.title("Ứng dụng chẩn đoán bệnh cây trồng")
    with st.container(border = True):
         uploaded_image = st.file_uploader("Kéo và thả", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.session_state.corrected_image = correct_orientation_and_resize(image)
        st.image(st.session_state.corrected_image, use_column_width=True)

    if st.button("Gửi", use_container_width=True):
        if uploaded_image is not None:
            encoded_image = encode_image(st.session_state.corrected_image)
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item = {
                'user_info': {
                    'user_name': st.session_state.get('user_name'),
                    'password': st.session_state.get('encrypted_password')
                },
                'image_info': {
                    'image': encoded_image,
                    'date': current_datetime
                }
            }
            with st.spinner("Đang phân tích hình ảnh..."):
                try:
                    results = analyze(item=item).json()

                    with st.container(border = True):
                        st.markdown("<div class='container'>", unsafe_allow_html=True)
                        st.session_state.predicted_image = decode_image(results['image_info']['predicted_image'])
                        class_prob = round(results['image_info']['class_prob'] * 100, 2)
                        st.image(st.session_state.predicted_image, caption=f'Vùng khả năng bị bệnh ({class_prob}%)', use_column_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with st.container(border = True):
                        st.markdown("<div class='container'>", unsafe_allow_html=True)
                        st.markdown("<h2>Tên Bệnh</h2>", unsafe_allow_html=True)
                        st.markdown(f"<p>{results['solution']['Tên bệnh']}</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with st.container(border = True):
                        st.markdown("<div class='container'>", unsafe_allow_html=True)
                        st.markdown("<h2>Mô Tả Bệnh</h2>", unsafe_allow_html=True)
                        st.markdown(f"<h4>Nguyên nhân</h4><p>{results['solution']['Mô tả']['cause']}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(f"<h4>Triệu chứng</h4><p>{results['solution']['Mô tả']['symptom']}</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with st.container(border = True):
                        st.markdown("<div class='container'>", unsafe_allow_html=True)
                        st.markdown("<h2>Giải Pháp</h2>", unsafe_allow_html=True)
                        st.markdown(f"<h4>Ngăn ngừa</h4><p>{results['solution']['Giải pháp']['prevention']}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(f"<h4>Làm vườn</h4><p>{results['solution']['Giải pháp']['gardening']}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(f"<h4>Phân bón</h4><p>{results['solution']['Giải pháp']['fertilization']}</p>", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(f"<h4>Nguồn</h4><p>{results['solution']['Giải pháp']['source']}</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                except KeyError as e:
                    st.error(f"Đã xảy ra lỗi khi phân tích hình ảnh: {e}")
        else:
            st.warning("Vui lòng tải lên một hình ảnh để tiến hành chẩn đoán.")

if __name__ == "__main__":
    app()
