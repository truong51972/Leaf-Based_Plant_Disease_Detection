import sqlite3
from datetime import datetime

PIC_PER_USER_LIMIT : int = 100

CONVERT_DICT = {'Tomato_mosaic_virus':1,
'Early_blight':2,
'Tomato_Yellow_Leaf_Curl_Virus':3,
'Late_blight':4,
'Bacterial_spot':5,
'Target_Spot':6,
'Septoria_leaf_spot':7,
'healthy':8,
'Leaf_Mold':9,
'Spider_mites_Two-spotted_spider_mite':10}

def add_picture_to_database(userName:str,  
                            class_name:str, 
                            picDate:datetime, 
                            pic:str, 
                            pred_pic:str, 
                            score:float,
                            con=sqlite3.connect('data.db')):
    '''
        This private function is used for adding picture information to database and delete picture if number of pictures per user exceed 100\n
        :input:
        userName : str,
        diseaseID: str,
        picDate: datetime (YYYY-MM-DD HH:MI:SS),
        pic: str (encrypted content of the pic),
        pred_pic: str (encrypted content of the pic),
        score: float ,
        con: sqlite3.connect(<database directory>)
        '''
    diseaseID = CONVERT_DICT[class_name]

    cur = con.cursor()
    
    formatted_time = datetime.strptime(picDate, '%Y-%m-%d %H:%M:%S')

    cur.execute(f"""
        INSERT INTO PIC (diseaseID, picDate, pic, pred_pic, score)
        VALUES ({diseaseID}, '{formatted_time}', '{pic}', '{pred_pic}', {score}) 
        """)

    con.commit()

    cur.execute(f'''
        SELECT last_insert_rowid()
        ''')
    
    picID = cur.fetchall()[0][0]

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{userName}'
        ''')
    
    userID = cur.fetchall()[0][0]

    con.commit()

    cur.execute(f'''
        INSERT INTO USER_PIC VALUES ({userID}, {picID})
        ''')
    
    con.commit()

    cur.execute(f'''
        SELECT * FROM USER_PIC WHERE userID = {userID}
    ''')

    if len(cur.fetchall()) > PIC_PER_USER_LIMIT:
        cur.execute(f'''
            SELECT picID FROM USER_PIC WHERE userID = {userID} ORDER BY picID ASC LIMIT 1
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



