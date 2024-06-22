import streamlit as st
import pandas as pd

def test():
    # Kiểm tra xem 'state' đã được khởi tạo chưa, nếu chưa thì khởi tạo
    if 'state' not in st.session_state:
        st.session_state.state = {
            'garden_num': 1,
            'line_num': 1
        }
    st.selectbox("134", ["vuon"]*10) 

    with st.container():
        st.subheader("Chọn Mảnh Vườn và Luống")
        col1, col2 = st.columns(2)
        
        with col1:
            garden_num = st.text_input("Thiết lập mảnh vườn", value=str(st.session_state.state['garden_num']))
        
        with col2:
            line_num = st.text_input("Thiết lập luống", value=str(st.session_state.state['line_num']))
        
        # Lưu giá trị mới vào session_state khi người dùng nhập vào
        st.session_state.state['garden_num'] = int(garden_num)
        st.session_state.state['line_num'] = int(line_num)

    # Khởi tạo DataFrame ban đầu
#     data = {
#         'Tên': ['Nam Gốc', 'Trường Cac Lo', 'Hiếu con chó', 'God Thiện'],
#         'luong 1': [1,0,1,0],
#         'Luống 2': [str(st.session_state.state['line_num'])] * 4
#     }
#     df = pd.DataFrame(data)

#     st.data_editor(
#         df,
#         column_config={
#             "luong 1": st.column_config.CheckboxColumn(
#                 "Your favorite?",
#                 help="Select your **favorite** widgets",
#                 default=False,
#             )
#         },
#         disabled=["widgets"],
#         hide_index=True,
# )
   

#     # Hiển thị DataFrame cho phép chỉnh sửa
#     edit_index = st.sidebar.selectbox('Chọn hàng để chỉnh sửa', df.index)
#     for col in df.columns:
#         new_value = st.sidebar.text_input(f'Nhập giá trị mới cho {col}', df.loc[edit_index, col])
#         df.loc[edit_index, col] = new_value

#     # Lưu thay đổi
#     st.write("### DataFrame")
#     st.write(df)

    data_df = pd.DataFrame(
        {
            "UserName": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
            "Luong1": [True, False, False, True],
            "Luong2": [True, False, False, True],
        }
    )

    st.data_editor(
        data_df,
        disabled=["widgets"],
        hide_index=True,
    )
# Chạy hàm test để hiển thị ứng dụng Streamlit
if __name__ == '__main__':
    test()
