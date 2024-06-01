import sqlite3

def reset_password(userName:str, newPassword:str, con):
    
    cur = con.cursor()

    cur.execute(f'''
    UPDATE USER
    SET userPassword = '{newPassword}'
    WHERE userName = '{userName}'
    ''')

    con.commit()


def main():
    class User():
            def __init__(self):
                self.user_name = 'hieu'
                self.password = '123'

    user = User()
    change_password(user, 'asd')

if __name__ == '__main__':
     main()
