import sqlite3
import asyncio
import pandas as pd
from datetime import datetime
from .__change_password import reset_password
from .__check_user import check_user
from .__check_password import check_password
from .__add_user import add_user
from .__extract_result import extract_result
from .__validate_password import validate_password
from .__extract_history import extract_history
from .__add_picture import add_picture_to_database
from .__extract_solution import get_solution_potato, get_solution_tomato
from .__get_statistic import get_statistic
from .__check_manager import is_manager
from .__extract_result_without_id import extract_result_without_id
from .__get_employee_list import get_employee
from .__load_employee_pic_count import load_employee_pic_count
from .__add_garden import add_garden_to_db
from .__get_garden_info import garden_info, garden_info_employee
from .__del_garden import del_garden
from .__del_employee import del_employee
from .__table import create_table, insert_assignment_table

### TASK CODE: unfinished, wait, pending

class Query:
    '''
    This class is used for interacting with database using various amount of functions

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
    '''

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
                 
    ### ADD SECTION ###
    async def add_user(self, item) -> dict:
        '''
            This private function is used for checking user password

            :input:
            item = {
            'manager_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        },
            'employee_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        }
            }

            :return:
            {'message': ...,
                'code': ...}

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '001': userName has already existed in the database (UserExisted)    
                '004': User has no authority (UnauthorizedAction)   
        '''   
        managerName = item.manager_info.user_name
        managerPassword = item.manager_info.password
        employeeName = item.employee_info.user_name
        employeePassword = item.employee_info.password
        

        if is_manager(managerName, self.con):
            if check_user(employeeName, self.con):
                return {'message':'userName already existed!',
                    'code':'001'}
            else:    
                add_user(managerName, employeeName, employeePassword, self.con)
                return {'message':'Success!',
                        'code':'000'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}
    
    async def add_garden(self, item):
        '''
        This function is used to add a garden with a number of lines and their manager
        :input:
        item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'garden_info' : {
            'plant_name' : str
            'garden_name' : str,
            'num_of_line' : int
        }
    }
        '''
        managerName = item.user_info.user_name
        managerPassword = item.user_info.password
        gardenName = item.garden_info.garden_name
        plantName = item.garden_info.plant_name
        lineID = list(range(1, item.garden_info.num_of_line+1))

        if is_manager(managerName, self.con):
            try:
                add_garden_to_db(managerName, gardenName, lineID, plantName, self.con)
                return {'message':'Success!',
                        'code' : '000'}
            except:
                return {'message':'gardenName already exist or line_num is invalid',
                        'code' : '102'}
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
            'predicted_image': str,
            'class_name': str,
            'score': float,
            'threshold': float,
            'plant_name': str,
            'garden_name': str,
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
        gardenName = item.image_info.garden_name
        lineID = item.image_info.line_num
        threshold = item.image_info.threshold
        plantName = item.image_info.plant_name

        if is_save is True:
            picID = add_picture_to_database(userName, class_name, picDate, pic, pred_pic, score, gardenName, lineID, self.con)
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

    ### QUERY and FUNCTIONAL SECTION ###
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
                        'is_manager':is_manager(userName, self.con)}
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
            {'message':'Success!',
             'code' : '000',
             'employee_info':{
                'employee_id': list[int],
                'employee_name': list[str]
                            }      
                    }

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '001': userName has already existed in the database (UserExisted)    
                '004': User has no authority (UnauthorizedAction)   
        '''
        managerName = managerData.user_name
        managerPassword = managerData.password

        if is_manager(managerName, self.con):
            employeeID_list, employeeName_list = get_employee(managerName, self.con)
            return {'message':'Success!',
                    'code' : '000',
                    'employee_info':{
                        'ID': employeeID_list,
                        'Tên nhân viên': employeeName_list
                                    }      
                    }
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    async def assign_employee_location(self, item):
        '''
            This function is used to assign employee to work location(s)

            :input:
            item = {
            'user_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        },
            'table': {
                "Tên Nhân Viên": ['employeeName1, employeeName2', ...],
                "Hàng 1": [bool, bool, ...],
                "Hàng 2": [bool, bool, ...],
                ...
                },
            'garden_name' : str
        }

            :return:
            {'message': ...,
                'code': ...}

            PERFORMANCE CODE:
                '000': Action proceeded successfully
                '003': userName doesn't exist in the database (UserNotFound)
                '101': Employee has already been assigned in the selected location (EmployeeLocationExisted)
        '''
        managerName = item.user_info.user_name
        managerPassword = item.user_info.password
        gardenName = item.garden_name

        table = pd.DataFrame(item.table)

        if is_manager(managerName, self.con):
            try:
                insert_assignment_table(gardenName, table, self.con)
                return {'message':'Success!',
                        'code':'000'}
            except:
                return {'message':'Employee has already been assigned in the selected location!',
                        'code' : '101'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}
          
    async def get_location_assignment_table(self, item):
        '''
        :input:
        item = {
            'user_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        },
            'garden_name' : str
        }
        :output:
        dict = {
            'message': str,
            'code': str,
            'table': {
                "Tên Nhân Viên": ['employeeName1, employeeName2', ...],
                "Hàng 1": [bool, bool, ...],
                "Hàng 2": [bool, bool, ...],
                ...
                }
        }
        '''
        managerName = item.user_info.user_name
        managerPassword = item.user_info.password
        gardenName = item.garden_name

        if is_manager(managerName, self.con):
            try:
                table = create_table(gardenName, managerName, self.con)
                return {'message':'Success!',
                        'code' : '000',
                        'table': table}
            except:
                return {'message':'Unknown error in del_garden()!',
                        'code' : '???'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    async def get_garden_info(self, item):
        '''
        This function is used for getting garden info, including num_of_line, gardenName, plantName

        :input:
        item = {
            'user_info':{
                'user_name': str,
                'password' : str
            }

        :output:
            {'message': str,
             'code': str,
             'garden_info':{
                    'Tên vườn' : list[str],
                    'Giống cây': list[str],
                    'Số luống' : list[int]
                }
             }
            or

        '''
        userName = item.user_info.user_name
        userPassword = item.user_info.password

        if is_manager(userName, self.con):
            gardenName, plantName, line_count = garden_info(userName, self.con)
            return {'message':'Success!',
                    'code' : '000',
                    'garden_info':{
                        'Tên vườn' : gardenName,
                        'Giống cây': plantName,
                        'Số luống' : line_count
                    }}
        else:
            gardenInfo = garden_info_employee(userName, self.con)
            return {'message':'Success!',
                    'code' : '000',
                    'garden_info': gardenInfo}

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
        score,
        lineID,
        gardenName,
        plantName) = extract_history(userName, self.con)     

        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'history': {
                    'Ảnh gốc' : pic,
                    'Tên bệnh' : class_name,
                    'Ảnh phân tích': pred_pic,
                    'Độ tin cậy': score,
                    'Ngày chụp' : picDate,
                    'Hàng': lineID,
                    'Tên vườn': gardenName,
                    'Giống cây': plantName
                           }
                }
    # pending
    async def get_statistic(self, item):
        '''
        :input:
    item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'start_date': 'YYYY-MM-DD',
        'end_date': 'YYYY-MM-DD',
        'garden_name': str
    }
        :output:
        {
        'code': str,
        'message': str,
        'statistic' : {
                        'overall_data' : dict(key, value),
                        'per_line' : {
                            'Hàng 1' : {
                                'Khoẻ' : int,
                                'Bệnh' : int,
                                'Chi tiết' : {
                                    dict('Tên bệnh' : số lượng)
                                }
                            },
                            'Hàng 2' : {
                                'Khoẻ' : int,
                                'Bệnh' : int,
                                'Chi tiết' : {
                                    dict('Tên bệnh' : số lượng)
                                }               
                            }
                        }
                    }
        '''
        userName = item.user_info.user_name
        userPassword = item.user_info.password
        startDate = item.start_date + ' 00:00:00'
        endDate = item.end_date + ' 23:59:59'
        gardenName = item.garden_name

        if is_manager(userName, self.con):
            statistic = get_statistic(startDate, endDate, gardenName, self.con)
            return {'message':'Success!',
                    'code' : '000',
                    'statistic': statistic}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    
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
    # pending
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
                'tasks_info':{
                    'userName': list,
                    'gardenName': list,
                    'lineID': list,
                    'pic_count': list
                    }
            }
        '''
        managerName = managerData.user_name
        managerPassword = managerData.password

        if is_manager(managerName, self.con):
            try:
                userName, gardenName, lineID, picCount = load_employee_pic_count(managerName, self.con)
                return {
                'tasks_info':{
                    'userName': userName,
                    'gardenName': gardenName,
                    'lineID': lineID,
                    'pic_count': picCount
                    }
            }
            except:
                return {'message':'Unknown error in del_garden()!',
                        'code' : '???'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    async def get_solution(self):
        '''
        :return:
        Dataframe / Dictionary of tuples:
        {
        'Cà chua': {
            'diseaseName' :         tuple(diseaseName), 
            'diseaseCause':         tuple(diseaseCause),
            'diseaseSymptom':       tuple(diseaseSymptom), 
            'solutionPrevention':   tuple(solutionPrevention),
            'solutionGardening':    tuple(solutionGardening),
            'solutionFertilization':tuple(solutionFertilization),
            'solutionSource':       tuple(solutionSource)
        },
        'Khoai tây': {
            'diseaseName' :         tuple(diseaseName), 
            'diseaseCause':         tuple(diseaseCause),
            'diseaseSymptom':       tuple(diseaseSymptom), 
            'solutionPrevention':   tuple(solutionPrevention),
            'solutionGardening':    tuple(solutionGardening),
            'solutionFertilization':tuple(solutionFertilization),
            'solutionSource':       tuple(solutionSource)
        }}
        '''
        return {
                'Cà chua': get_solution_tomato(self.con),
                'Khoai tây': get_solution_potato(self.con)
                }
    
    ### DELETE SECTION ###
    async def delete_garden(self, item):
        '''
        :input:
        item = {
            'user_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        },
            'garden_name' : str
        }

        :output:
        {'message':str, 
         'code': str}
        '''

        managerName = item.user_info.user_name
        managerPassword = item.user_info.password
        gardenName = item.garden_name

        if is_manager(managerName, self.con):
            try:
                del_garden(gardenName, self.con)
                return {'message':'Success!',
                        'code' : '000'}
            except:
                return {'message':'Unknown error in del_garden()!',
                        'code' : '???'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}

    async def delete_user(self, item):
        '''
            This function is used for delete user from database

            :input:
            item = {
            'manager_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        },
            'employee_info': {
                'user_name' : 'user name',
                'password' : 'password'
                        }
            }

            :output:
            {'message':str, 
             'code': str}

            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '001': userName has already existed in the database (UserExisted)    
                '004': User has no authority (UnauthorizedAction)   
        '''

        managerName = item.manager_info.user_name
        managerPassword = item.manager_info.password
        employeeName = item.employee_info.user_name
        employeePassword = item.employee_info.password

        if is_manager(managerName, self.con):
            try:
                del_employee(employeeName, self.con)
                return {'message':'Success!',
                        'code' : '000'}
            except:
                return {'message':'Unknown error in del_employee()!',
                        'code' : '???'}
        else:
            return {'message':'User has no authority!',
                    'code' : '004'}
    
    def close(self):
        self.con.commit()
        self.con.close() 

def main():
    pass

if __name__ == '__main__':
    main()