import sqlite3

def identify_location(gardenName:str, lineID:int, con) -> int:
    cur = con.cursor()

    cur.execute(f'''
                SELECT gardenID
                FROM GARDEN
                WHERE gardenName = '{gardenName}'
                ''')
    
    gardenID = cur.fetchall()[0][0]

    cur.execute(f'''
                SELECT locationID 
                FROM LOCATION 
                WHERE gardenID = {gardenID} and lineID = {lineID}
                ''')
    
    locationID = cur.fetchall()[0][0]

    return locationID