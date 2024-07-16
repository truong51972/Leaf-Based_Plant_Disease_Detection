import streamlit as st
from datetime import datetime, timedelta
from packages.request_api import get_statistics, get_gardens_info
from packages.__request import _request
import pandas as pd
import plotly.express as px # type: ignore

def fetch_gardens_statistics():
    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        }
    }
    response = get_gardens_info(item=item, request=_request).json()
    
    if 'garden_info' not in response:
        st.warning("Không có dữ liệu vườn.")
        return []

    garden_info = response['garden_info']
    garden_names = garden_info.get('Tên vườn', [])
    return garden_names

def statistics_ui():
    if 'user_name' not in st.session_state or 'encrypted_password' not in st.session_state:
        st.warning("Vui lòng đăng nhập để xem thống kê.")
        return

    st.subheader("Thống kê của bạn")

    garden_names = fetch_gardens_statistics()
    
    if not garden_names:
        st.warning("Không có dữ liệu vườn.")
        return
    
    selected_garden_name = st.selectbox("Chọn vườn", garden_names, key='statistic_garden')

    selected_date = st.date_input("Vui lòng chọn ngày để xem thống kê.", datetime.today() - timedelta(days=1), key='start_date')
    end_date = st.date_input("Vui lòng chọn ngày kết thúc để xem thống kê.", datetime.today(), key='end_date')

    selected_date_str = selected_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    select_threshold = st.selectbox("Chọn cây", options=[True, False], format_func=lambda x: 'Cây dự đoán đạt chuẩn' if x else 'Cây dự đoán không đạt chuẩn', key='threshold')

    

    item = {
        'user_info': {
            'user_name': st.session_state.get('user_name'),
            'password': st.session_state.get('encrypted_password')
        },
        'start_date': selected_date_str,
        'end_date': end_date_str,
        'garden_name': selected_garden_name,
        'is_over_threshold':select_threshold
    }

    st.markdown("<hr style='border: 2px solid #ccc;'>", unsafe_allow_html=True)
    response = get_statistics(item=item, request=_request)
    
    if response.status_code == 200:
        data = response.json()
        
        overall_data_json = data.get('statistic', {}).get('overall_data', {})
        if not overall_data_json:
            st.warning("Không có dữ liệu thống kê.")
            return

        df_overall = pd.DataFrame.from_dict(overall_data_json, orient='index').fillna(0)
        
        df_overall.reset_index(inplace=True)
        df_overall_melted = df_overall.melt(id_vars='index', var_name='Tình trạng', value_name='Số lượng')
        
        fig = px.bar(df_overall_melted, 
                     x='index', 
                     y='Số lượng', 
                     color='Tình trạng', 
                     orientation='v',
                     hover_data={'Số lượng': True, 'Tình trạng': True, 'index': False},
                     title=f'Giá trị của các loại bệnh của vườn: {selected_garden_name}')
        
        fig.update_layout(
            xaxis_title='Hàng', 
            yaxis_title='Giá trị', 
            yaxis=dict(showticklabels=True),
            hovermode='closest',
            showlegend=False,
            font=dict(
                family="Times New Roman",
                size=12,
                color="black",
                weight="bold"   
            )
        )          

        st.plotly_chart(fig, use_container_width=True, responsive=True)
    
        st.markdown("<hr style='border: 2px solid #ccc;'>", unsafe_allow_html=True)
        per_line_data = data.get('statistic', {}).get('per_line', {})
        st.subheader("Dữ liệu chi tiết")
        
        selected_row = st.selectbox("Chọn hàng để xem chi tiết", list(per_line_data.keys()))
        line_data = per_line_data.get(selected_row, {})
        
        st.subheader(f"Tình trạng chi tiết của: {selected_row}")
        
        labels = ['Khỏe', 'Bệnh']
        values = [
            line_data.get('Khỏe', 0),
            line_data.get('Bệnh', 0)
        ]
        
        fig_pie = px.pie(names=labels, values=values)
        fig_pie.update_traces(textinfo='percent')
               
        detail_data = line_data.get('Chi tiết', {})
        df_detail = pd.DataFrame(detail_data.items(), columns=['Loại bệnh', 'Số lượng']).fillna(0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')      
            st.dataframe(df_detail, hide_index=True)
