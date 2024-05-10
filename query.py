import sqlite3

class UserLogin:
    def __init__(self) -> None:
        pass

    def __get_user_login(self, userName:str, userPassword:str):
        pass

    def __generate_key(self):
        pass

    def __get_key(self):
        pass

    def __encode(self) -> bytes:
        pass

    def __decode(self):
        pass

    def __check_user_availability(self, userName:str):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
    SELECT userName from USER  
    """)    
        user = cur.fetchone()
        print(type(user))
        print(user)
        con.commit()
        con.close()

        if userName in user:
            return True
        else:
            return False

    def __check_password(self, encodedPassword:bytes):
        pass

    def __add_user(self, userName:str, userPassword:str):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
    INSERT INTO USER VALUES ({userName}, {self.__encode(userPassword)})  
    """)
        con.commit()
        con.close()

    def add_user(self, userName:str, userPassword:str):
        if self.__check_user_availability(userName):
            raise Exception('Username has already been used. Please use another username.')
        else:
            self.__add_user(userName, userPassword)

    def user_login(self, userName:str, userPassword:str):
        if self.__check_user_availability(userName):
            encodedPassword = self.__encode(userPassword)
            if self.__check_password(encodedPassword):
                return True
            else:
                return False
        else:
            raise Exception('User not available. Registeration is recommended.')
        
    def check(self, userName:str):
        return self.__check_user_availability(userName)


print(UserLogin().check('34234234'))

