import sqlite3
from datetime import datetime

def add_picture_to_database(picID, class_name, picDate, pic, pred_pic, class_prob, con):
    '''
        This private function is used for adding picture information to database
        :input:
        picID: int,
        class_name: int,
        picDate: datetime (YYYY-MM-DD HH:MI:SS)
        pic: str (enscripted content of the pic)
        '''
    
    cur = con.cursor()
    
    formatted_time = datetime.strptime(picDate, '%Y-%m-%d %H:%M:%S')

    cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, '{class_name}', '{formatted_time}', '{pic}', '{pred_pic}', {class_prob}) 
        """)

    con.commit()