import sqlite3
from datetime import datetime

# Check if userName exists in database
# return True/False
def __check_user(userName:str, database='data.db') -> bool:
    con = sqlite3.connect(database)
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

# Check if password is correct
# return True/False
def __check_password(userName:str, userPassword:str, database='data.db') -> bool:
    con = sqlite3.connect(database)
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

# Add user to database
# return 'status'
def add_user(userData, database='data.db') -> dict:
    '''
        PERFORMANCE CODE:
            '000': Action proceeded successfully 
            '001': userName has already existed in the database (UserExisted)
    '''
    userName = userData.user_name
    userPassword = userData.password

    # Inner function to add user to database
    def __add_user(userName:str, userPassword:str, database):
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(f"""
    INSERT INTO USER VALUES ({userName}, {userPassword})  
    """)
        con.commit()
        con.close()

    if __check_user(userName):
        return {'message':'userName already existed!',
                'code':'001'}
    else:
        __add_user(userName, userPassword)
        return {'message':'Success!',
                'code':'000'}

# Login function
# return 'status'
def user_login(userData, database='data.db') -> dict:
    '''
        PERFORMANCE CODE:
            '000': Action proceeded successfully 
            '002': userPassword doesn't match with the userName in the database (WrongPassword)
            '003': userName doesn't exist in the database (UserNotFound)
    '''

    userName = userData.user_name
    userPassword = userData.password

    if __check_user(userName, database):
        if __check_password(userName, userPassword, database):
            return {'message':'Success!',
                    'code':'000'}
        else:
            return {'message':'Wrong password!',
                    'code':'002'}
    else:
        return {'message':'userName not exist!',
                'code':'003'}

def main():
    current_time = datetime.now()

    # Định dạng thời gian theo YYYY-MM-DD HH:MI:SS
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    print(formatted_time)
   
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    cur.execute(f"""
    INSERT INTO PIC VALUES (0, 0, {formatted_time}, 'abc') 
    """)

    con.commit()
    con.close()

if __name__ == '__main__':
    main()
