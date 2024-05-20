import sqlite3

def check_user(userName:str, database='data.db') -> bool:
    '''
        This private function is used for checking user existence in database

            :input:
            userName: str,
            userPassword: str

            :return:
            type(bool)
        '''  
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(f"""
    SELECT userName from USER  
    """)    
    user = cur.fetchall()
    con.commit()
    con.close()

    if (userName,) in user:
        return True
    else:
        return False