import streamlit as st
from packages.request_api import get_history
from packages.__request import _request
import pandas as pd

def __url_gen(x):
    return 'data:image/jpeg;base64,' + x

def display_history():
    select_threshold = st.selectbox("Chọn cây", options=[True, False], format_func=lambda x: 'Cây dự đoán đạt chuẩn' if x else 'Cây dự đoán không đạt chuẩn', key='threshold')
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        },
        'is_over_threshold':select_threshold
    }
    
    if st.button("Xem thông tin"):
        response =  get_history(item=item,request=_request).json()
        
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
