import streamlit as st
from packages.request_api import get_history
import pandas as pd
import pytz

def __url_gen(x):
    return 'data:image/jpeg;base64,' + x

def utc(dt):
    local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    dt_local = local_tz.localize(dt)
    return dt_local.astimezone(pytz.utc).astimezone(local_tz)

def display_history():
    item = {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    
    if st.button("Xem thông tin."):
        response =  get_history(item=item).json()
        
        df_history = pd.DataFrame(response['history'])

        if 'Ngày chụp' in df_history.columns:
            df_history['Ngày chụp'] = pd.to_datetime(df_history['Ngày chụp'])
            df_history['Ngày chụp'] = df_history['Ngày chụp'].apply(lambda x: utc(x))
        

        df_history['Ảnh gốc'] = df_history['Ảnh gốc'].apply(__url_gen)
        df_history['Ảnh phân tích'] = df_history['Ảnh phân tích'].apply(__url_gen)

        st.data_editor(
            df_history,
            column_config={
                'Ngày chụp': st.column_config.DatetimeColumn(format='YYYY-MM-DD HH:mm:ss', timezone='Asia/Ho_Chi_Minh'),
                'Ảnh gốc': st.column_config.ImageColumn(width='small'),
                'Ảnh phân tích':st.column_config.ImageColumn(width='small')
            },
            hide_index=True,
        )
