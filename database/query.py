import sqlite3

# Check if userName exists in database
# return True/False
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

# Check if password is correct
# return True/False
def check_password(userName:str, userPassword:str) -> bool:
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute(f"""
    SELECT userPassword from USER WHERE userName = '{userName}'
    """)    
    password = cur.fetchone()
    print(password[0])
    con.commit()
    con.close()

    if userPassword == password[0]:
        return True
    else:
        return False

# Add user to database
# return 'status'
def add_user(userName:str, userPassword:str) -> dict:
    '''
        PERFORMANCE CODE:
            '000': Action proceeded successfully 
            '001': userName has already existed in the database (UserExisted)
    '''
    # Inner function to add user to database
    def __add_user(userName:str, userPassword:str):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
    INSERT INTO USER VALUES ({userName}, {userPassword})  
    """)
        con.commit()
        con.close()

    if check_user(userName):
        return {'message':'userName already existed!',
                'code':'001'}
    else:
        __add_user(userName, userPassword)
        return {'message':'Success!',
                'code':'000'}

# Login function
# return 'status'
def user_login(userName:str, userPassword:str) -> dict:
    '''
        PERFORMANCE CODE:
            '000': Action proceeded successfully 
            '002': userPassword doesn't match with the userName in the database (WrongPassword)
            '003': userName doesn't exist in the database (UserNotFound)
    '''
    if check_user(userName):
        if check_password(userPassword):
            return {'message':'Success!',
                    'code':'000'}
        else:
            return {'message':'Wrong password!',
                    'code':'002'}
    else:
        return {'message':'userName not exist!',
                'code':'003'}
    
'''
    PERFORMANCE CODE:
        '000': Action proceeded successfully 

        Login code:
            '001': userName has already existed in the database (UserExisted)
            '002': userPassword doesn't match with the userName in the database (WrongPassword)
            '003': userName doesn't exist in the database (UserNotFound)
'''

def main():
   print(check_password('abc', 'zxy')) 

if __name__ == '__main__':
    main()
