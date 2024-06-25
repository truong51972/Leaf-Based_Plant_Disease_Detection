import sqlite3

def identify_location(gardenName:str, lineID:int, con) -> int:
    cur = con.cursor()

    cur.execute(f'''
                SELECT locationID 
                FROM LOCATION 
                WHERE gardenID = '{gardenName}' and lineID = {lineID}
                ''')
    
    locationID = cur.fetchall()[0][0]

    return locationID