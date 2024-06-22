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
from .__get_statistic import get_statistic
from .__check_manager import is_manager
from .__extract_result_without_id import extract_result_without_id
from .__assign_location import assign_location
from .__get_employee_list import get_employee
from .__load_employee_pic_count import load_employee_pic_count

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
            managerData, newUserInfo: User()
                        
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
            if check_user(newUserName, self.con):
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
                'code': ...,
                'is_manager': bool}

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '002': userPassword doesn't match with the userName in the database (WrongPassword)
                '003': userName doesn't exist in the database (UserNotFound)
        '''

        userName = userData.user_name
        userPassword = userData.password

        if not check_user(userName, self.con):
            return {'message':'userName not exist!',
                    'code':'003',
                    'is_manager':False} 
        else:
            if check_password(userName, userPassword, self.con):
                return {'message':'Success!',
                        'code':'000',
                        'is_manager':is_manager(userName)}
            else:
                return {'message':'Wrong password!',
                        'code':'002',
                        'is_manager':False}
            
    async def get_employee_list(self, managerData):
        '''
            This private function is used for getting list of employee based on managerData

            :input:
            managerData: User()
                        
            NOTE:
            class User():
                def __init__(self):
                    self.user_name = ...
                    self.password = ...

            :return:
            employee_list : list = [...]

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '001': userName has already existed in the database (UserExisted)    
                '004': User has no authority (UnauthorizedAction)   
        '''
        managerName = managerData.user_name
        managerPassword = managerData.password

        if is_manager(managerName, self.con):
            return get_employee(managerName, self.con)
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

            
    async def assign_employee_location(self, managerData, employeeData, location):
        '''
            This function is used to assign employee to work location(s)

            :input:
            managerData, employeeData: User()
            location = {
                    'gardenNum': int = ...,
                    'lineNum': int = ...
                }
                        
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
                '003': userName doesn't exist in the database (UserNotFound)
                '101': Employee has already been assigned in the selected location (EmployeeLocationExisted)
        '''
        managerName = managerData.user_name
        managerPassword = managerData.password
        employeeName = employeeData.user_name
        employeePassword = employeeData.password

        gardenNum = location.gardenNum
        lineNum = location.lineNum

        if is_manager(managerName, self.con):
            try:
                assign_location(employeeName, gardenNum, lineNum, self.con)
                return {'message':'Success!',
                        'code':'000'}
            except:
                return {'message':'Employee has already been assigned in the selected location!',
                        'code' : '101'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    async def add_pic_and_get_solution(self, item, is_save):   
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
            'class_name': str,
            'score': float,
            'predicted_image': str,
            'garden_num': int,
            'line_num': int
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
        gardenNum = item.image_info.garden_num
        lineNum = item.image_info.line_num

        if is_save is True:
            picID = add_picture_to_database(userName, class_name, picDate, pic, pred_pic, score, gardenNum, lineNum, self.con)
            class_name, description, solution = extract_result(picID, self.con)
        else:
            class_name, description, solution = extract_result_without_id(class_name, self.con)
        
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
        This function is used to get history of a user.
    
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

        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'history': {
                    'Ảnh gốc' : pic,
                    'Tên bệnh' : class_name,
                    'Ảnh phân tích': pred_pic,
                    'Độ tin cậy': score,
                    'Ngày chụp' : picDate
                           }
                }
    
    async def get_statistic(self, item):
        '''
        :input:
    item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'date': 'YYYY-MM-DD',
        'gardenNum': int,
        'lineNum': int
    }
        :output:
        statistic = {'Virus khảm cà chua ToMV': int = ..., 
                 'Bệnh bạc lá sớm': int = ..., 
                 'Virus TYLCV (Tomato yellow leaf curl virus)': int = ..., 
                 'Bệnh tàn rụi muộn': int = ..., 
                 'Đốm vi khuẩn': int = ..., 
                 'Nấm Corynespora': int = ..., 
                 'Nấm Septoria lycopersici': int = ..., 
                 'Cây tốt': int = ..., 
                 'Bệnh khuôn lá': int = ..., 
                 'Bệnh nhện đỏ': int = ...}
        '''
        userName = item.user_info.user_name
        userPassword = item.user_info.password
        date = item.date

        validate_result = validate_password(userName, userPassword, self.con)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                    }
        statistic = get_statistic(userName,date, self.con)
        return statistic
    
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
    
    async def load_employee_pic_count(self, managerData):
        '''
        This function is used to load picture count per employee for each location

        :input:
            managerData: User()
                        
            NOTE:
            class User():
                def __init__(self):
                    self.user_name = ...
                    self.password = ...

        :return:
            dict_dataframe = {
                'userName': list,
                'gardenNum': list,
                'lineNum': list,
                'pic_count': list
            }
        '''
        managerName = managerData.user_name
        managerPassword = managerData.password

        if is_manager(managerName, self.con):
            return load_employee_pic_count(managerName, self.con)
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    
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
    

    def close(self):
        self.con.commit()
        self.con.close() 

def main():
    pass

if __name__ == '__main__':
    main()