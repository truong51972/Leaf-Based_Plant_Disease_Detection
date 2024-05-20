import streamlit as st
from packages.request_api import get_history
import pandas as pd

def __url_gen(x):
    return 'data:image/jpeg;base64,' + x

def time_zone():
    server_timezone = pytz.timezone('UTC')
    server_time = datetime.utcnow()

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
