import streamlit as st
from PIL import Image, ExifTags
from datetime import datetime
from packages.encode_decode import encode_image, decode_image
from packages.request_api import analyze, get_gardens_info
from packages.__request import _request
import pytz

guard = """
        ### Hướng dẫn chụp ảnh
        1. **Cách chụp**: Chụp ảnh với tỷ lệ 1:1.
        2. **Chọn ảnh**: Phải chọn ảnh là lá cà chua hoặc khoai tây.
        3. **Ánh sáng tốt**: Chụp ảnh dưới ánh sáng tự nhiên, tránh ánh sáng mạnh trực tiếp hoặc bóng râm quá nhiều.
        4. **Tiêu cự gần**: Chụp ảnh lá ở khoảng cách gần để thấy rõ chi tiết.
        5. **Nền đơn giản**: Đặt lá lên nền đơn giản để không bị nhiễu bởi các vật thể khác.
        6. **Chụp toàn bộ lá**: Chụp từ trên xuống để thấy rõ toàn bộ bề mặt lá.
        7. **Tránh che khuất hoặc làm mờ lá**: Đảm bảo không che khuất những điểm bị bệnh.
        """

def correct_orientation_and_resize(image):
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
    
    image = image.resize((224, 224), Image.BILINEAR)
    return image

def display_results(results):
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.session_state.predicted_image = decode_image(results['image_info']['predicted_image'])
    

    if 'image_info' in results and isinstance(results['image_info'], dict):
        score = results['image_info'].get('score')
        threshold = results['image_info'].get('threshold')
        
        if score is not None and threshold is not None:
            score = round(score, 4)
            threshold = round(threshold, 4)
            
            st.image(st.session_state.predicted_image, use_column_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='container'>", unsafe_allow_html=True)
            
            st.markdown("<h2>Kết quả dự đoán</h2>", unsafe_allow_html=True)
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
        else:
            st.error("Có vẻ ảnh của bạn không hợp lệ. Vui lòng thử lại với một ảnh khác.")
    else:
        st.error("Có vẻ ảnh của bạn không hợp lệ. Vui lòng thử lại với một ảnh khác.")

def fetch_gardens():
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }
    response = get_gardens_info(item=item, request=_request).json()
    garden_info = response.get('garden_info', {})
    return garden_info

def app():
    st.title("Khám bệnh lá online!")
    gardens = fetch_gardens()
    
    try:
        if not gardens:
            st.warning("Nhân viên hiện chưa được phân công. Liên hệ với quản lý để được hỗ trợ.")
            return
        
        with st.container(border=True):
            garden_names = list(gardens.keys())
            selected_garden = st.selectbox("Chọn vườn", garden_names, key='garden_app')
            
            if selected_garden not in gardens:
                st.warning("Vườn đã chọn không tồn tại trong danh sách vườn. Vui lòng chọn lại.")
                return
            
            garden_details = gardens[selected_garden]
            plant_name = garden_details['Giống cây']

            lines = [int(line.split()[-1]) for line in garden_details['Luống'] if line.split()[-1].isdigit()]
            selected_line = st.selectbox("Chọn luống", lines, key='line_app')

            st.write(f'Giống cây: {plant_name}')
            
        with st.container(border=True):    
            uploaded_image = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png"], help=guard)
    
            if uploaded_image is not None:
                image = Image.open(uploaded_image)
                
                if plant_name.lower() not in ['cà chua', 'khoai tây']:
                    st.warning("Vui lòng chọn ảnh lá cà chua hoặc khoai tây để tiếp tục.")
                    return
                
                st.session_state.corrected_image = correct_orientation_and_resize(image)
                st.image(st.session_state.corrected_image, use_column_width=True)    
            
            if st.button("Gửi", use_container_width=True):
                if selected_garden is None:
                    st.warning("Vui lòng chọn một vườn để tiếp tục.")
                    return
                
                if uploaded_image is None:
                    st.warning("Vui lòng tải lên một hình ảnh để tiến hành chẩn đoán.")
                    return
                
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
                        'plant_name': plant_name,
                        'garden_name': selected_garden,
                        'line_num': selected_line
                    }
                }
                
                with st.spinner("Đang phân tích hình ảnh..."):
                    try:
                        results = analyze(item=item, request=_request).json()                        
                        display_results(results)
                    except KeyError as e:
                        st.error(f"Đã xảy ra lỗi khi phân tích hình ảnh: {e}")
                    except Exception as e:
                        st.error(f"Đã xảy ra lỗi không xác định: {e}")
    
    except Exception as e:
        st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")

if __name__ == "__main__":
    app()