import sqlite3
import asyncio
from datetime import datetime

class Query:
    '''
    This class is used for interacting with database using various amount of functions

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database) 
    '''

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database)
        
    def __check_user(self, userName:str) -> bool:
        '''
            This private function is used for checking user existence in database

            :input:
            userName: str,
            userPassword: str

            :return:
            type(bool)
        '''  
        self.cur = self.con.cursor()
        self.cur.execute(f"""
        SELECT userName from USER  
        """)    
        user = self.cur.fetchall()
        self.con.commit()

        if (userName,) in user:
            return True
        else:
            return False
                     
    def __check_password(self, userName:str, userPassword:str) -> bool:
        '''
            This private function is used for checking user password

            :input:
            userName: str,
            userPassword: str

            :return:
            type(bool)
            '''  
        self.cur = self.con.cursor()         
        self.cur.execute(f"""
            SELECT userPassword from USER WHERE userName = '{userName}'
        """)    
        password = self.cur.fetchone()

        self.con.commit()         

        if userPassword == password[0]:
            return True
        else:
            return False
        
    def __add_user(self, userName:str, userPassword:str):
        '''
            This private function is used for adding user into database

            :input:
            userName: str,
            userPassword: str
            '''  
        self.cur = self.con.cursor()
        self.cur.execute(f"""
            INSERT INTO USER VALUES ('{userName}', '{userPassword}')  
        """)
        self.con.commit()
    
    def __picID_list_len(self):
            '''
            This private function is used for getting number of pictures saved in database

            :return:
            list_len: int
            '''  
            self.cur = self.con.cursor()

            self.cur.execute(f"""
            SELECT picID FROM PIC
            """)

            picID_list = self.cur.fetchall()
            list_len = len(picID_list)

            self.con.commit()

            return list_len
    
    def __extract_result(self, picID:int):  
            '''
            This private function is used for extract result with known picID

            :input:
            picID: int

            :return:
            tuple(prediction: dict, class_name: str, description: dict, solution: dict)

            NOTE:
            prediction = {
                'pred_pic': pred_pic,
                'class_prob': class_prob
            }
            description = {
                'cause':diseaseCause,
                'symptom':diseaseSymptom                
            }
            solution = {
                'prevention':solutionPrevention,
                'gardening':solutionGardening,
                'fertilization':solutionFertilization,
                'source':solutionSource
            }
            '''  
            self.cur = self.con.cursor()

            self.cur.execute(f"""
            select picID,
                   pred_pic,
                   class_prob,                   
                   diseaseName, 
                   diseaseCause, 
                   diseaseSymptom, 
                   solutionPrevention,
                   solutionGardening,
                   solutionFertilization,
                   solutionSource
            from
            (
            select * from 
            (
                PIC join DISEASE on PIC.class_name=DISEASE.class_name
            )
                join SOLUTION on SOLUTION.class_name=PIC.class_name
            )
            where picID = 1
            """)

            data_list = self.cur.fetchall()[0]
            (pred_pic,
             class_prob,
             diseaseName, 
             diseaseCause,
             diseaseSymptom, 
             solutionPrevention,
             solutionGardening,
             solutionFertilization,
             solutionSource) = (
                 data_list[1],
                 data_list[2],
                 data_list[3],
                 data_list[4],
                 data_list[5],
                 data_list[6],
                 data_list[7],
                 data_list[8],
                 data_list[9],
                 ) 
            
            prediction = {
                'pred_pic': pred_pic,
                'class_prob': class_prob
            }
            class_name = diseaseName
            description = {
                'cause':diseaseCause,
                'symptom':diseaseSymptom                
            }
            solution = {
                'prevention':solutionPrevention,
                'gardening':solutionGardening,
                'fertilization':solutionFertilization,
                'source':solutionSource
            }

            self.con.commit()

            return prediction, class_name, description, solution
    
    def __validate_password(self, userName, userPassword) -> dict:
        '''
            This private function is used for validating user

            :input:
            userName: str,
            userPassword: str

            :return:
            type(bool)
            '''  
        if not self.__check_user(userName):
            return {'message':'userName not exist!',
                    'code':'003'} 
        else:
            if self.__check_password(userName, userPassword):
                return {'message':'Success!',
                        'code':'000'}
            else:
                return {'message':'Wrong password!',
                        'code':'002'}  
                 
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
        
        if self.__check_user(userName):
            return {'message':'userName already existed!',
                    'code':'001'}
        else:
            self.__add_user(userName, userPassword)
            return {'message':'Success!',
                    'code':'000'}

    def __user_login(self, userData) -> dict:
        '''
            This private function is used for user login

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

        if not self.__check_user(userName):
            return {'message':'userName not exist!',
                    'code':'003'} 
        else:
            if self.__check_password(userName, userPassword):
                return {'message':'Success!',
                        'code':'000'}
            else:
                return {'message':'Wrong password!',
                        'code':'002'}

    def __get_history(self, userData):
        '''
        :return:
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob,
        cause,
        symptom,
        prevention,
        gardening, 
        fertilization,
        source)
        '''
        userName = userData.user_name
        userPassword = userData.password

        if userName == 'admin':
            
            self.cur.execute(f'''
            select userName, 
                   picDate, 
                   pic, 
                   pred_pic,
                   class_prob,
                   diseaseName, 
                   diseaseCause, 
                   diseaseSymptom, 
                   solutionGardening, 
                   solutionPrevention, 
                   solutionFertilization, 
                   solutionSource
            from USER_PIC
            join PIC on USER_PIC.picID = PIC.picID
            join DISEASE on PIC.class_name=DISEASE.class_name
            join SOLUTION on SOLUTION.class_name=DISEASE.class_name
            order by picDate desc
            
            ''')

            history = self.cur.fetchall()
            self.con.commit()
        
        else:
            self.cur.execute(f'''
            select userName, 
                   picDate, 
                   pic, 
                   pred_pic,
                   class_prob,
                   diseaseName, 
                   diseaseCause, 
                   diseaseSymptom, 
                   solutionGardening, 
                   solutionPrevention, 
                   solutionFertilization, 
                   solutionSource
            from USER_PIC
            join PIC on USER_PIC.picID = PIC.picID
            join DISEASE on PIC.class_name=DISEASE.class_name
            join SOLUTION on SOLUTION.class_name=DISEASE.class_name
            where userName = '{userName}'
            order by picDate desc
            
            ''')
            history = self.cur.fetchall()
            self.con.commit()
        
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob,
        cause,
        symptom,
        prevention,
        gardening, 
        fertilization,
        source) = ([], [], [], [], [], [], [], [], [], [], [])

        for index, attribute in enumerate(
        [pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob,
        cause,
        symptom,
        prevention,
        gardening, 
        fertilization,
        source]):
            for i in history:
                attribute.append(i[index+1])

        return (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob,
        cause,
        symptom,
        prevention,
        gardening, 
        fertilization,
        source)

    def __add_picture_to_database(self, picID, class_name, picDate, pic, pred_pic, class_prob):
        '''
        This private function is used for adding picture information to database
        :input:
        picID: int,
        class_name: int,
        picDate: datetime (YYYY-MM-DD HH:MI:SS)
        pic: str (enscripted content of the pic)
        '''
    
        # formatted time: YYYY-MM-DD HH:MI:SS
        formatted_time = datetime.strptime(picDate, '%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        self.cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, {class_name}, '{formatted_time}', '{pic}', '{pred_pic}', {class_prob}) 
        """)

        self.con.commit()
    
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

        validate_result = self.__validate_password(userName, userPassword)
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
        picID = self.__picID_list_len()

        self.__add_picture_to_database(picID, class_name, picDate, pic, pred_pic, pred_acc)

        self.cur.execute(f'''
        INSERT INTO USER_PIC VALUES ('{userName}', {picID})
        ''')
        self.con.commit()

        prediction, class_name, description, solution = self.__extract_result(picID)
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
    
    async def login_and_get_history(self, userData):
        login = self.__user_login(userData)
        if login['code'] == '002' or login['code'] == '003':
            return {
                'message' : login['message'],
                'code': login['code'],
                    }
        # history = {'message' : 'message!',
        #            'code': 'error code!',
        #            'result': {
        #                 'class_name' : None,
        #                 'accuracy': None,
        #                 'predicted_image': None,
        #                 'description' : None,
        #                 'solution' : None
        #                     }
        #             }
        message = login['message']
        code = login['code']
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob,
        cause,
        symptom,
        prevention,
        gardening, 
        fertilization,
        source) = self.__get_history(userData)       

        return {
                'message' : login['message'],
                'code': login['code'],
                'history': {
                    'Ảnh Gốc' : pic,
                    'Ảnh Phân Tích': pred_pic,
                    'Độ Tin Cậy': class_prob,
                    'Ngày Chụp' : picDate,
                    'Tên Bệnh' : class_name    
                           }
                }

    def close(self):
        self.con.commit()
        self.con.close() 

def main():
    a = ['aed', 'aeda', 'aewvww']
    b = list(zip(a, range(len(a))))
    print(b)

if __name__ == '__main__':
    main()