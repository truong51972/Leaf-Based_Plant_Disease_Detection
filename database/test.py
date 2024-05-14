def main():
    import sqlite3
    from datetime import datetime
    def is_password_correct(userName:str, userPassword:str) -> bool:
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
        
    def is_exist_user(userName:str) -> bool:
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

    def add_picture(picData):
    
        picID = picData.id
        diseaseID = picData.diseaseID
        picDate = picData.date
        pic = picData.pic

        # Định dạng thời gian theo YYYY-MM-DD HH:MI:SS
        formatted_time = picDate.strftime('%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, {diseaseID}, '{formatted_time}', '{pic}') 
        """)

        con.commit()
        con.close()

    # class User:
    #     def __init__(self) -> None:
    #         self.user_name = 'admin'
    #         self.password = 'xW2PqVk-e29mqX3T2aZAYPuBl5e4SKVeKDXfvU9XC9g'

    class Pic:
        def __init__(self) -> None:
            self.id = 66
            self.diseaseID = 1
            self.date = datetime.now()
            self.pic = 'lmao'

    pic = Pic()

    add_picture(pic)


if __name__ == '__main__':
    # async def read_results():
    #     loop = asyncio.get_event_loop()
    #     results = await loop.run_in_executor(None, some_library) # type: ignore
    #     return results
    main()