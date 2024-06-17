import sqlite3

def check_user(userName:str, con=sqlite3.connect('data.db')) -> bool:
    '''
        This private function is used for checking user existence in database

            :input:
            userName: str,
            userPassword: str,
            con: sqlite3.connect(<database directory>)

            :return:
            type(bool)
        '''  
    cur = con.cursor()
    cur.execute(f"""
    SELECT userName from USER  
    """)    
    user = cur.fetchall()
    con.commit()


    if (userName,) in user:
        return True
    else:
        return False