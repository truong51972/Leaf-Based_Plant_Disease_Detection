import re

def is_valid(text: str):
    # Biểu thức chính quy kiểm tra ký tự đặc biệt
    special_characters = '[ _!#$%^&*()<>?/\|}{~:,.' + "'" + '"' + ']'
    regex = re.compile(special_characters)
    
    # Nếu chuỗi chứa ký tự đặc biệt thì trả về True
    if(regex.search(text) == None):
        return True
    else: 
        return False
    
if __name__ == '__main__':
    s = "Hello World"
    print(is_valid(s))  # Trả về True
