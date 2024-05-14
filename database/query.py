import sqlite3
import asyncio
from datetime import datetime

class Query:

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database)
        
    def __check_user(self, userName:str) -> bool:
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
        self.cur = self.con.cursor()
        self.cur.execute(f"""
            INSERT INTO USER VALUES ('{userName}', '{userPassword}')  
        """)
        self.con.commit()
                 
    async def add_user(self, userData) -> dict:
        '''
        PERFORMANCE CODE:
            '000': Action proceeded successfully 
            '001': userName has already existed in the database (UserExisted)
        '''

    
        userName = userData.user_name
        userPassword = userData.password

    # Inner function to add user to database
        if self.__check_user(userName):
            return {'message':'userName already existed!',
                    'code':'001'}
        else:
            self.__add_user(userName, userPassword)
            return {'message':'Success!',
                    'code':'000'}

    async def user_login(self, userData) -> dict:
        '''
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

    async def add_picture(self, picData):
    
        picID = picData.id
        diseaseID = picData.diseaseID
        picDate = picData.date
        pic = picData.pic
    
        # Định dạng thời gian theo YYYY-MM-DD HH:MI:SS
        formatted_time = picDate.strftime('%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        self.cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, {diseaseID}, '{formatted_time}', '{pic}') 
        """)

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