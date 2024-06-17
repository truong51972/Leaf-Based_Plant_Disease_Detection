import sqlite3

def check_password(userName:str, 
                   userPassword:str, 
                   con=sqlite3.connect('data.db')) -> bool:
        '''
            This private function is used for checking user password

            :input:
            userName: str,
            userPassword: str,
            con: sqlite3.connect(<database directory>)

            :return:
            type(bool)
            '''  

        cur = con.cursor()         
        cur.execute(f"""
            SELECT userPassword from USER WHERE userName = '{userName}'
        """)    
        password = cur.fetchone()

        con.commit()         

        if userPassword == password[0]:
            return True
        else:
            return False