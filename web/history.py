import streamlit as st
import pandas as pd

def __url_gen(x):
    return 'data:image/jpeg;base64,' + x

def display_history():

    if st.button("Tải lại trang"):
        pass
 
    df_history = pd.DataFrame(st.session_state['history'])

    df_history['Ngày Chụp'] = df_history['Ngày Chụp'].apply(__url_gen)
    df_history['Tên Bệnh'] = df_history['Tên Bệnh'].apply(__url_gen)

    st.data_editor(
    df_history,
    column_config={
        'Ngày Chụp': st.column_config.ImageColumn(width='small'),
        'Tên Bệnh':st.column_config.ImageColumn(width='small')
    },
    hide_index=True,
)
