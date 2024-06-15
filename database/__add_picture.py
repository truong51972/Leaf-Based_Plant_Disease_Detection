import sqlite3
from datetime import datetime

PIC_PER_USER_LIMIT : int = 100

def add_picture_to_database(userName:str, 
                            picID:int, 
                            class_name:str, 
                            picDate:datetime, 
                            pic:str, 
                            pred_pic:str, 
                            class_prob:float,
                            con):
    '''
        This private function is used for adding picture information to database and delete picture if number of pictures per user exceed 100\n
        :input:
        userName : str,
        picID: int,
        class_name: str,
        picDate: datetime (YYYY-MM-DD HH:MI:SS),
        pic: str (encrypted content of the pic),
        pred_pic: str (encrypted content of the pic),
        class_prob: float ,
        con: sqlite3.connect(<database directory>)
        '''
    
    cur = con.cursor()
    
    formatted_time = datetime.strptime(picDate, '%Y-%m-%d %H:%M:%S')

    cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, '{class_name}', '{formatted_time}', '{pic}', '{pred_pic}', {class_prob}) 
        """)

    con.commit()

    cur.execute(f'''
        INSERT INTO USER_PIC VALUES ('{userName}', {picID})
        ''')
    
    con.commit()

    cur.execute(f'''
        SELECT * FROM USER_PIC WHERE userName = '{userName}'
    ''')

    if len(cur.fetchall()) > PIC_PER_USER_LIMIT:
        cur.execute(f'''
            SELECT picID FROM USER_PIC WHERE userName = '{userName}' ORDER BY picID ASC LIMIT 1
        ''')
    
        deleted_id = cur.fetchall()[0][0]

        con.commit()

        cur.execute(f'''
        DELETE FROM USER_PIC 
        WHERE picID = {deleted_id}
        ''')
        con.commit()

        cur.execute(f'''
        DELETE FROM PIC 
        WHERE picID {deleted_id}
        ''')
        con.commit()

        cur.execute(f'''
        UPDATE PIC 
        SET picID = picID - 1 
        WHERE picID > {deleted_id} 
        ''')
        con.commit()

        cur.execute(f'''
        UPDATE USER_PIC 
        SET picID = picID - 1 
        WHERE picID > {deleted_id} 
        ''')
        con.commit()



