import sqlite3

def add_user(managerName:str,
             newUserName:str, 
             newUserPassword:str, 
             con=sqlite3.connect('data.db')):
    '''
            This private function is used for adding user into database

            :input:
            managerName: str,
            newUserName: str,
            newUserPassword: str,
            con: sqlite3.connect(<database directory>)
            '''  
    cur = con.cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    managerID = cur.fetchall()[0][0]

    cur.execute(f"""
            INSERT INTO USER (userName, userPassword, managerID) VALUES ('{newUserName}', '{newUserPassword}', {managerID})  
        """)
    con.commit()
