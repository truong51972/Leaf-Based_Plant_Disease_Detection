import sqlite3
import asyncio
from datetime import datetime
from .__change_password import reset_password
from .__check_user import check_user
from .__check_password import check_password
from .__add_user import add_user
from .__extract_result import extract_result
from .__validate_password import validate_password
from .__extract_history import extract_history
from .__add_picture import add_picture_to_database
from .__extract_solution import get_solution
from .__get_statistics import get_statistic
from .__check_manager import is_manager

class Query:
    '''
    This class is used for interacting with database using various amount of functions

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
    '''

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
                 
    async def add_user(self, managerData, newUserInfo) -> dict:
        '''
            This private function is used for checking user password

            :input:
            userData, newUserInfo: User()
                        
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
                '004': User has no authority (UnauthorizedAction)   
        '''   
        managerName = managerData.user_name
        managerPassword = managerData.password
        newUserName = newUserInfo.user_name
        newUserPassword = newUserInfo.password
        

        if is_manager(managerName, self.con):
            if check_user(managerName, self.con):
                return {'message':'userName already existed!',
                    'code':'001'}
            else:    
                add_user(managerName, newUserName, newUserPassword, self.con)
                return {'message':'Success!',
                    'code':'000'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}
            

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
            'score': None,
            'predicted_image': None
        }
    }

    :return:
    {
    'message' : 'message!',
    'code': 'error code!',
    'result': {
        'class_name' : str or None,
        'score': float or None,
        'predicted_image': str or None,
        'description' : (type = dictionary) or None,
        'solution' : (type = dictionary) or None
    }
    }'''             

        userName = item.user_info.user_name
        userPassword = item.user_info.password

        validate_result = validate_password(userName, userPassword, self.con)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }

        pred_pic = item.image_info.predicted_image
        score = item.image_info.score
        pic = item.image_info.image
        picDate = item.image_info.date
        class_name = item.image_info.class_name

        picID = add_picture_to_database(userName, class_name, picDate, pic, pred_pic, score, self.con)

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
        '''
        This function is used to change password of a user.
    
    :input:
    userData = {
            'user_name' : 'user name',
            'password' : 'password'
    }
    :return:
    If the user validation is True:
                {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'history': {
                    'Ảnh gốc' : pic,
                    'Tên bệnh' : class_name,
                    'Ảnh phân tích': pred_pic,
                    'Độ tin cậy': score,
                    'Ngày chụp' : picDate
                           },
                'statistics':{
                    'date1':{
                        'disease1': number_of_disease1,
                        'disease2': number_of_disease2,
                        ...
                            },
                    'date2':{
                        ...
                            },
                    ...
                            }
                }
    Else:
                {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                }
        '''
        
        userName = userData.user_name
        userPassword = userData.password

        validate_result = validate_password(userName, userPassword, self.con)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        score) = extract_history(userData, self.con)

        statistic = get_statistic(userName, self.con)       

        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'history': {
                    'Ảnh gốc' : pic,
                    'Tên bệnh' : class_name,
                    'Ảnh phân tích': pred_pic,
                    'Độ tin cậy': score,
                    'Ngày chụp' : picDate
                           },
                'statistic': statistic
                }
    
    async def change_password(self, item):
        '''
        This function is used to change password of a user.
    
    :input:
    item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'new_password' : 'new_password'
    }
        '''

        userName = item.user_info.user_name
        userPassword = item.user_info.password
        newPassword = item.new_password

        validate_result = validate_password(userName, userPassword, self.con)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }
        
        reset_password(userName, newPassword, self.con)
        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }
    
    async def get_solution(self):
        '''
        :return:
        Dataframe / Dictionary of tuples:
        {
        'diseaseName' :         tuple(diseaseName), 
        'diseaseCause':         tuple(diseaseCause),
        'diseaseSymptom':       tuple(diseaseSymptom), 
        'solutionPrevention':   tuple(solutionPrevention),
        'solutionGardening':    tuple(solutionGardening),
        'solutionFertilization':tuple(solutionFertilization),
        'solutionSource':       tuple(solutionSource)
        }
        '''
        return get_solution(self.con)
    

    async def close(self):
        self.con.commit()
        self.con.close() 

def main():
    pass

if __name__ == '__main__':
    main()