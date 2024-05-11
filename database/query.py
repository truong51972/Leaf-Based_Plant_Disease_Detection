import sqlite3
import asyncio
from datetime import datetime

class Query:

    def __init__(self, database='data.db'):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    async def __check_user(self, userName:str) -> bool:
        self.cur.execute(f"""
        SELECT userName from USER  
        """)    
        user = self.cur.fetchone()

        if userName in user:
            return True
        else:
            return False
                     
    async def __check_password(self, userName:str, userPassword:str) -> bool:
                 
        self.cur.execute(f"""
            SELECT userPassword from USER WHERE userName = '{userName}'
        """)    
        password = self.cur.fetchone()
                 

        if userPassword == password[0]:
            return True
        else:
            return False
        
    async def __add_user(self, userName:str, userPassword:str):
        self.cur.execute(f"""
            INSERT INTO USER VALUES ('{userName}', '{userPassword}')  
        """)
                 
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

        if self.__check_user(userName):
            if self.__check_password(userName, userPassword):
                return {'message':'Success!',
                        'code':'000'}
            else:
                return {'message':'Wrong password!',
                        'code':'002'}
        else:
            return {'message':'userName not exist!',
                    'code':'003'}  

    async def add_picture(self, picData):
    
        picID = picData.id
        diseaseID = picData.diseaseID
        picDate = picData.date
        pic = picData.pic
    
        current_time = datetime.now()

        # Định dạng thời gian theo YYYY-MM-DD HH:MI:SS
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        self.cur.execute(f"""
        INSERT INTO PIC VALUES (1, 1, '{formatted_time}', 'abc') 
        """)

    async def close(self):
        self.con.commit()
        self.con.close() 


async def main():
    class User:
        def __init__(self) -> None:
            self.user_name = 'admin'
            self.password = 'xW2PqVk-e29mqX3T2aZAYPuBl5e4SKVeKDXfvU9XC9g='
    user = User()

    query = Query()
    await query.check_user(user)

    '''
    import asyncio

    async def __main():
        await asyncio.sleep(10, result='hello')

    asyncio.run(__main())
    '''

if __name__ == '__main__':
    # async def read_results():
    #     loop = asyncio.get_event_loop()
    #     results = await loop.run_in_executor(None, some_library) # type: ignore
    #     return results
    main()