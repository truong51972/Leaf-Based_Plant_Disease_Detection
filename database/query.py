import sqlite3
import asyncio
from datetime import datetime

class Query:

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
            self.con = sqlite3.connect('data.db')
            self.cur = self.con.cursor()

            self.cur.execute(f"""
            SELECT picID FROM PIC
            """)

            picID_list = self.cur.fetchall()
            list_len = len(picID_list)

            self.con.commit()
            self.con.close()

            return list_len
    
    def __extract_result(self, picID:int):  
            '''
            This private function is used for extract result with known picID

            :input:
            picID: int

            :return:
            tuple(class_name: str, description: dict, solution: dict)

            NOTE:
            description = {
                'cause':diseaseCause,
                'symptom':diseaseSymptom                
            }
            solution = {
                'prevention':solutionPreventation,
                'gardening':solutionGardening,
                'fertilization':solutionFertilization,
                'source':solutionSource
            }
            '''  
            self.con = sqlite3.connect('data.db')
            self.cur = self.con.cursor()

            self.cur.execute(f"""
            select picID,
                   diseaseName, 
                   diseaseCause, 
                   diseaseSymptom, 
                   solutionPreventation,
                   solutionGardening,
                   solutionFertilization,
                   solutionSource
            from
            (
            select * from 
            (
                PIC join DISEASE on PIC.diseaseID=DISEASE.diseaseID
            )
                join SOLUTION on SOLUTION.diseaseID=PIC.diseaseID
            )
            where picID = {picID}
            """)

            data_list = self.cur.fetchall()[0]
            (diseaseName, 
             diseaseCause,
             diseaseSymptom, 
             solutionPreventation,
             solutionGardening,
             solutionFertilization,
             solutionSource) = (
                 data_list[1],
                 data_list[2],
                 data_list[3],
                 data_list[4],
                 data_list[5],
                 data_list[6],
                 data_list[7]
                 ) 
            
            class_name = diseaseName
            description = {
                'cause':diseaseCause,
                'symptom':diseaseSymptom                
            }
            solution = {
                'prevention':solutionPreventation,
                'gardening':solutionGardening,
                'fertilization':solutionFertilization,
                'source':solutionSource
            }

            self.con.commit()
            self.con.close()

            return class_name, description, solution
    
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

    async def user_login(self, userData) -> dict:
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

    async def __add_picture_to_database(self, picID, diseaseID, picDate, pic):
        '''
        This private function is used for adding picture information to database
        :input:
        picID: int,
        diseaseID: int,
        picDate: datetime (YYYY-MM-DD HH:MI:SS)
        pic: str (enscripted content of the pic)
        '''
    
        # formatted time: YYYY-MM-DD HH:MI:SS
        formatted_time = picDate.strftime('%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        self.cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, {diseaseID}, '{formatted_time}', '{pic}') 
        """)
    
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
            'class_name': None
        }
    }

    :return:
    {
    'message' : 'message!',
    'code': 'error code!',
    'result': {
        'class_name' : 'class name' or None,
        'description' : (type = dictionary) or None,
        'solution' : (type = dictionary) or None
    }
    }'''             

        userName = item['user_info']['user_name']
        userPassword = item['user_info']['password']

        validate_result = self.__validate_password(userName, userPassword)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'result': {
                    'class_name' : None,
                    'description' : None,
                    'solution' : None
                        }
                    }

        pic = item.image_info.image
        picDate = item.image_info.date
        diseaseID = item.image_info.class_name
        picID = self.__picID_list_len()

        self.__add_picture_to_database(picID, diseaseID, picDate, pic)
        class_name, description, solution = self.__extract_result(picID)
        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'result': {
                    'class_name' : class_name,
                    'description' : description,
                    'solution' : solution
                          }
                }

    async def close(self):
        self.con.commit()
        self.con.close() 


def main():
    
    def check_password(userName:str, userPassword:str) -> bool:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
            SELECT userPassword from USER WHERE userName = '{userName}'
        """)    
        password = cur.fetchone()
        con.commit()
        con.close() 

        if userPassword == password[0]:
            return True
        else:
            return False
        
    def check_user(userName:str) -> bool:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
        SELECT userName from USER  
        """)    
        user = cur.fetchone()
        con.commit()
        con.close() 
        if userName in user:
            return True
        else:
            return False
        
    def user_login(userData) -> dict:
        '''
            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '002': userPassword doesn't match with the userName in the database (WrongPassword)
                '003': userName doesn't exist in the database (UserNotFound)
        '''

        userName = userData.user_name
        userPassword = userData.password

        print(userName, userPassword)

        # if not check_user(userName):
        #     if check_password(userName, userPassword):
        #         return {'message':'Success!',
        #                 'code':'000'}
        #     else:
        #         return {'message':'Wrong password!',
        #                 'code':'002'}
        # else:
        #     return {'message':'userName not exist!',
        #             'code':'003'} 
        if not check_user(userName):
            return {'message':'userName not exist!',
                    'code':'003'} 
        else:
            if check_password(userName, userPassword):
                return {'message':'Success!',
                        'code':'000'}
            else:
                return {'message':'Wrong password!',
                        'code':'002'}
    class User:
        def __init__(self) -> None:
            self.user_name = 'admin'
            self.password = 'xW2PqVk-e29mqX3T2aZAYPuBl5e4SKVeKDXfvU9XC9g'
    user = User()
    query = Query()

    print(query.user_login(user))
    
    # print(user.user_name, user.password)
    # print(type(user.user_name), type(user.password))

    # print(check_user(user.user_name))  
    # #print(check_password('admi', user.password))
    
    # if not check_user(user.user_name):
    #         print( {'message':'userName not exist!',
    #                 'code':'003'} )
    # else:
    #     if check_password(user.user_name, user.password):
    #         print({'message':'Success!',
    #                 'code':'000'})
    #     else:
    #         print( {'message':'Wrong password!',
    #                 'code':'002'})
    # print(user_login(user))

    # class User:
    #     def __init__(self) -> None:
    #         self.user_name = 'admin'
    #         self.password = 'xW2PqVk-e29mqX3T2aZAYPuBl5e4SKVeKDXfvU9XC9g='
    # user = User()

    # query = Query()
    # await query.check_user(user)



if __name__ == '__main__':
    # async def read_results():
    #     loop = asyncio.get_event_loop()
    #     results = await loop.run_in_executor(None, some_library) # type: ignore
    #     return results
    main()