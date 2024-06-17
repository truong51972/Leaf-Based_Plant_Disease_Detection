import sqlite3

def reset_password(userName:str, 
                   newPassword:str, 
                   con=sqlite3.connect('data.db')):
    '''
            This private function is used for adding user into database

            :input:
            userName: str,
            userPassword: str,
            con: sqlite3.connect(<database directory>)
            '''  
    cur = con.cursor()

    cur.execute(f'''
    UPDATE USER
    SET userPassword = '{newPassword}'
    WHERE userName = '{userName}'
    ''')

    con.commit()


def main():
    pass

if __name__ == '__main__':
    main()
