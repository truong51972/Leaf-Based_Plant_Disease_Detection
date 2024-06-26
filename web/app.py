import streamlit as st
from PIL import Image, ExifTags
from datetime import datetime
from packages.encode_decode import encode_image, decode_image
from packages.request_api import analyze, get_gardens_info
import pytz

guard = """
        ### Hướng dẫn chụp ảnh
        1. **Cách chụp**: Chụp ảnh với tỷ lệ 1:1.
        2.**Chọn ảnh**: Phải chọn ảnh là lá cà chua hoặc khoai tây
        3. **Ánh sáng tốt**: Chụp ảnh dưới ánh sáng tự nhiên, tránh ánh sáng mạnh trực tiếp hoặc bóng râm quá nhiều.
        4. **Tiêu cự gần**: Chụp ảnh lá ở khoảng cách gần để thấy rõ chi tiết.
        5. **Nền đơn giản**: Đặt lá lên nền đơn giản để không bị nhiễu bởi các vật thể khác.
        6. **Chụp toàn bộ lá**: Chụp từ trên xuống để thấy rõ toàn bộ bề mặt lá.
        7. **Tránh che khuất hoặc làm mờ lá**: Đảm bảo không che khuất những điểm bị bệnh.
        """

def correct_orientation_and_resize(image, max_size=(224, 224)):
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

def display_results(results):
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.session_state.predicted_image = decode_image(results['image_info']['predicted_image'])
    score = round(results['image_info']['score'], 4)
    threshold = round(results['image_info']['threshold'], 4)
    
    st.image(st.session_state.predicted_image, use_column_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    
    st.markdown("<h2>Tên Bệnh</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{results['solution']['Tên bệnh']}</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h4>Giải thích</h4>", unsafe_allow_html=True)
    st.markdown(f"Điểm số: {score}", help="Điểm số là điểm của mô hình dự đoán.")
    st.markdown(f"Ngưỡng: {threshold}", help="Ngưỡng là điểm tổng quát đã được kiểm tra dựa trên dữ liệu thực tế.")
    
    if score > threshold:
        st.markdown(f"**Sự chắc chắn**: **Điểm số** đã vượt qua **ngưỡng**, điều này cho thấy mô hình rất tự tin chẩn đoán về **{results['solution']['Tên bệnh']}** trong trường hợp này.")
    else:
        st.markdown("Khả năng: **Điểm số** không vượt qua **ngưỡng**, bạn nên kiểm tra lại.")
        st.markdown("""
        **Lời khuyên**:
        1. Xem lại mục **Hướng dẫn chụp ảnh** để đảm bảo bạn đã chụp đúng cách.
        2. Thử chụp lại ảnh với chất lượng tốt hơn theo hướng dẫn.
        3. Nếu bạn vẫn không chắc chắn, hãy gửi ảnh này cho chuyên gia để được tư vấn thêm.
        """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("<h2>Mô Tả Bệnh</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4>Nguyên nhân</h4><p>{results['solution']['Mô tả']['cause']}</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<h4>Triệu chứng</h4><p>{results['solution']['Mô tả']['symptom']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

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

def fetch_gardens():
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }
    response = get_gardens_info(item=item).json()
    gardens = response['garden_info']
    return gardens

def app():
    st.title("Khám bệnh lá online!")
    gardens = fetch_gardens()
    
    if not gardens or not gardens.get("Tên vườn"):
        st.warning("Không có thông tin về vườn. Vui lòng thêm vườn trong phần quản lý.")
        return
    try:
        garden_names = gardens["Tên vườn"]
        selected_garden = st.selectbox("Chọn vườn", garden_names)
        
        garden_index = garden_names.index(selected_garden)
        num_of_lines = gardens["Số luống"][garden_index]
        
        lines = [i + 1 for i in range(num_of_lines)]
        selected_line = st.selectbox("Chọn luống", lines)
        
        uploaded_image = st.file_uploader("**Chọn ảnh**", type=["jpg", "jpeg", "png"], help= guard)
        
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.session_state.corrected_image = correct_orientation_and_resize(image)
            st.image(st.session_state.corrected_image, use_column_width=True)
        
        if st.button("Gửi", use_container_width=True):
            if uploaded_image is not None:
                encoded_image = encode_image(st.session_state.corrected_image)
                timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                current_datetime = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
                item = {
                    'user_info': {
                        'user_name': st.session_state.get('user_name'),
                        'password': st.session_state.get('encrypted_password')
                    },
                    'image_info': {
                        'image': encoded_image,
                        'date': current_datetime,
                        'garden_name': selected_garden,
                        'line_num':selected_line
                    }
                }
                
                with st.spinner("Đang phân tích hình ảnh..."):
                    try:
                        results = analyze(item=item).json()
                        display_results(results)
                    except KeyError as e:
                        st.error(f"Đã xảy ra lỗi khi phân tích hình ảnh: {e}")
            else:
                st.warning("Vui lòng tải lên một hình ảnh để tiến hành chẩn đoán.")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    app()