import sqlite3

def change_password(userName:str, newPassword:str, database='data.db'):
    
    con = sqlite3.connect(database)
    cur = con.cursor()

    cur.execute(f'''
    UPDATE USER
    SET userPassword = '{newPassword}'
    WHERE userName = '{userName}'
    ''')

    con.commit()
    con.close()

def main():
    class User():
            def __init__(self):
                self.user_name = 'hieu'
                self.password = '123'

    user = User()
    change_password(user, 'asd')

if __name__ == '__main__':
     main()
