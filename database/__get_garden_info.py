import sqlite3

def garden_info(managerName:str,
                con):
    cur = con.cursor()
    
    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    managerID = cur.fetchall()[0][0]

    cur.execute(f'''
        SELECT gardenName, plantName, count(*) as line_count
        FROM GARDEN 
        JOIN LOCATION on GARDEN.gardenID = LOCATION.gardenID
        WHERE managerID = {managerID}
        group by LOCATION.gardenID
        ''')
    
    data = cur.fetchall()

    gardenName = list(map(lambda x: x[0], data))
    plantName = list(map(lambda x: x[1], data))
    line_count = list(map(lambda x: x[2], data))

    return gardenName, plantName, line_count
