import sqlite3
from datetime import datetime
from .__identify_location import identify_location

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
                            gardenName:str,
                            lineID:int,
                            con) -> int:
    '''
        This private function is used for adding picture information to database and delete picture if number of pictures per user exceed 100\n
        :input:
        userName : str,
        class_name: str,
        picDate: datetime (YYYY-MM-DD HH:MI:SS),
        pic: str (encrypted content of the pic),
        pred_pic: str (encrypted content of the pic),
        score: float,
        gardenNum:int,
        lineNum:int,
        con: sqlite3.connect(<database directory>)

        :return:
        picID: int
        '''
    diseaseID = CONVERT_DICT[class_name]

    cur = con.cursor()
    
    formatted_time = datetime.strptime(picDate, '%Y-%m-%d %H:%M:%S')

    locationID = identify_location(gardenName, lineID, con)

    cur.execute(f"""
        INSERT INTO PIC (diseaseID, picDate, pic, pred_pic, score, locationID)
        VALUES ({diseaseID}, '{formatted_time}', '{pic}', '{pred_pic}', {score}, {locationID}) 
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

    return picID



