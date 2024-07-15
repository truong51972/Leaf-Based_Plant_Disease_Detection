import streamlit as st
import pandas as pd
from packages.request_api import get_all_solutions
from packages.__request import _request

def solution_list():
    st.title("Các giải pháp cho các bệnh cây trồng")

    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }

    plant_options = ["Cà chua", "Khoai tây"]
    selected_plant = st.selectbox("Chọn loại cây:", plant_options)

    if selected_plant:
        st.subheader(f"Giải pháp cho {selected_plant}")
        try:
            response = get_all_solutions(item=item, request=_request).json()

            if not response or selected_plant not in response:
                st.warning(f"Không có dữ liệu giải pháp cho {selected_plant}.")
                return

            disease_data = response[selected_plant]

            if 'Tên Bệnh' not in disease_data:
                st.error(f"'Tên Bệnh' key not found in disease data: {disease_data}")
                return

            disease_names = list(disease_data['Tên Bệnh'])
            selected_disease = st.selectbox(f"Chọn bệnh của {selected_plant}:", disease_names)

            if selected_disease:
                disease_index = disease_names.index(selected_disease)

                details = {
                    'Nguyên Nhân': disease_data['Nguyên Nhân'][disease_index],
                    'Triệu Chứng': disease_data['Triệu Chứng'][disease_index],
                    'Phòng Ngừa': disease_data['Phòng Ngừa'][disease_index],
                    'Làm Vườn': disease_data['Làm Vườn'][disease_index],
                    'Phân Bón': disease_data['Phân Bón'][disease_index],
                    'Nguồn': disease_data['Nguồn'][disease_index]
                }

                df_solution = pd.DataFrame(list(details.items()), columns=['Tiêu Đề', 'Thông Tin'])

                st.table(df_solution.set_index('Tiêu Đề').style.set_properties(**{'text-align': 'left', 'font-size': '14px'}))

        except Exception as e:
            st.error(f"Lỗi khi lấy dữ liệu giải pháp cho {selected_plant}: {str(e)}")