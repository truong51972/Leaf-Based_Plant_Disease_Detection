import sqlite3

def add_garden_to_db(managerName:str,
                     gardenName:str, 
                     lineID:list[int],
                     plantName:str, 
                     con):
    
    cur = con.cursor()
    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    managerID = cur.fetchall()[0][0]

    cur.execute(f'''
                INSERT INTO GARDEN (gardenName, managerID, plantName)
                VALUES ('{gardenName}', {managerID}, '{plantName}')
                ''')
    
    con.commit()

    cur.execute(f'''
        SELECT last_insert_rowid()
        ''')
    
    gardenID = cur.fetchall()[0][0]

    for line in lineID:
        cur.execute(f'''
                    INSERT INTO LOCATION (gardenID, lineID)
                    VALUES ({gardenID}, {line})
                    ''')
        


        con.commit()