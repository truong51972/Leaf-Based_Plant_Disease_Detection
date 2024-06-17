import streamlit as st
from packages.request_api import get_history
from streamlit import cache
import pandas as pd

def __url_gen(x):
    return 'data:image/jpeg;base64,' + x

@st.cache
def get_first_upload_date():
    item = {
        'user_name': st.session_state.get('user_name'),
        'password': st.session_state.get('encrypted_password')
    }

    response = get_history(item=item).json()

    if 'history' in response:
        df_history = pd.DataFrame(response['history'])

        if not df_history.empty:
            last_row = df_history.iloc[-1]
            first_upload_date = last_row['Ngày chụp']
            st.write(f"Ngày đầu tiên gửi ảnh vào ứng dụng: {first_upload_date}")
        else:
            st.warning("Không có dữ liệu lịch sử để hiển thị.")
    else:
        st.error("Lỗi khi lấy dữ liệu lịch sử.")

def display_history():
    item = {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    
    if st.button("Xem thông tin"):
        response =  get_history(item=item).json()
        
        df_history = pd.DataFrame(response['history'])

        df_history['Ảnh gốc'] = df_history['Ảnh gốc'].apply(__url_gen)
        df_history['Ảnh phân tích'] = df_history['Ảnh phân tích'].apply(__url_gen)

        st.data_editor(
            df_history,
            column_config={
                'Ảnh gốc': st.column_config.ImageColumn(width='small'),
                'Ảnh phân tích':st.column_config.ImageColumn(width='small')
            },
            hide_index=True,
        )
