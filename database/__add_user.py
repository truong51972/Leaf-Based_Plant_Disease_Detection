import sqlite3

def add_user(userName:str, userPassword:str, database='data.db'):
    '''
            This private function is used for adding user into database

            :input:
            userName: str,
            userPassword: str
            '''  
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(f"""
            INSERT INTO USER VALUES ('{userName}', '{userPassword}')  
        """)
    con.commit()
    con.close()