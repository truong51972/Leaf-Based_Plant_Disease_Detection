import sqlite3

def identify_location(gardenNum:int, lineNum:int, con) -> int:
    cur = con.cursor()

    cur.execute(f'''
                SELECT locationID 
                FROM LOCATION 
                WHERE gardenNum = {gardenNum} and lineNum = {lineNum}
                ''')
    
    locationID = cur.fetchall()[0][0]

    return locationID