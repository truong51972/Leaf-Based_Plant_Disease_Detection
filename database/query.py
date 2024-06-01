import sqlite3
import asyncio
from datetime import datetime
from __change_password import change_password
from __check_user import check_user
from __check_password import check_password
from __add_user import add_user
from __picID_len import picID_list_len
from __extract_result import extract_result
from __validate_password import validate_password
from __extract_history import extract_history
from __add_picture import add_picture_to_database

class Query:
    '''
    This class is used for interacting with database using various amount of functions

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
    '''

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
                 
    async def add_user(self, userData) -> dict:
        '''
            This private function is used for checking user password

            :input:
            userData: User()
                        
            NOTE:
            class User():
                def __init__(self):
                    self.user_name = ...
                    self.password = ...

            :return:
            {'message': ...,
                'code': ...}

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '001': userName has already existed in the database (UserExisted)       
        '''   
        userName = userData.user_name
        userPassword = userData.password
        
        if check_user(userName, self.con):
            return {'message':'userName already existed!',
                    'code':'001'}
        else:
            add_user(userName, userPassword, self.con)
            return {'message':'Success!',
                    'code':'000'}

    async def user_login(self, userData) -> dict:
        '''
            This function is used for user login

            :input:
            userData: User()
                        
            NOTE:
            class User():
                def __init__(self):
                    self.user_name = ...
                    self.password = ...

            :return:
            {'message': ...,
                'code': ...}

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '002': userPassword doesn't match with the userName in the database (WrongPassword)
                '003': userName doesn't exist in the database (UserNotFound)
        '''

        userName = userData.user_name
        userPassword = userData.password

        if not check_user(userName, self.con):
            return {'message':'userName not exist!',
                    'code':'003'} 
        else:
            if check_password(userName, userPassword, self.con):
                return {'message':'Success!',
                        'code':'000'}
            else:
                return {'message':'Wrong password!',
                        'code':'002'}
    
    async def add_pic_and_get_solution(self, item):   
        '''
    This function is used to add picture to database and extract solution for that picture.
    
    :input:
    item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'image_info' : {
            'image' : 'decoded image',
            'date' : 'YYYY-MM-DD HH:MI:SS',
            'class_name': None,
            'accuracy': None,
            'predicted_image': None
        }
    }

    :return:
    {
    'message' : 'message!',
    'code': 'error code!',
    'result': {
        'class_name' : str or None,
        'class_prob': float or None,
        'predicted_image': str or None,
        'description' : (type = dictionary) or None,
        'solution' : (type = dictionary) or None
    }
    }'''             

        userName = item.user_info.user_name
        userPassword = item.user_info.password

        validate_result = validate_password(userName, userPassword)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }

        pred_pic = item.image_info.predicted_image
        pred_acc = item.image_info.class_prob
        pic = item.image_info.image
        picDate = item.image_info.date
        class_name = item.image_info.class_name
        picID = picID_list_len(self.con)

        add_picture_to_database(picID, class_name, picDate, pic, pred_pic, pred_acc, self.con)

        self.cur.execute(f'''
        INSERT INTO USER_PIC VALUES ('{userName}', {picID})
        ''')
        self.con.commit()

        class_name, description, solution = extract_result(picID, self.con)
        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'image_info' :item.image_info,
                'solution': {
                    'Tên bệnh' : class_name,                
                    'Mô tả' : description,
                    'Giải pháp' : solution
                           }
                }
    
    async def get_history(self, userData):
        userName = userData.user_name
        userPassword = userData.password

        validate_result = validate_password(userName, userPassword)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob) = extract_history(userData, self.con)       

        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'history': {
                    'Ảnh gốc' : pic,
                    'Tên bệnh' : class_name,
                    'Ảnh phân tích': pred_pic,
                    'Độ tin cậy': class_prob,
                    'Ngày chụp' : picDate
                           }
                }
    
    async def change_password(self, item):

        userName = item.user_info.user_name
        userPassword = item.user_info.password
        newPassword = item.new_password

        validate_result = validate_password(userName, userPassword)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }
        
        change_password(userName, newPassword, self.con)
        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }

    async def close(self):
        self.con.commit()
        self.con.close() 

def main():
    pass

if __name__ == '__main__':
    main()