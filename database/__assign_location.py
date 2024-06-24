import sqlite3
from .__identify_location import identify_location

def assign_location(employeeName:str,
                    gardenName:int,
                    lineID:int,
                    con):
    
    cur = con.cursor()

    cur.execute(f'''
                SELECT userID from USER where userName = '{employeeName}'
                ''')
    
    ID = cur.fetchall()
    employeeID = ID[0][0]

    cur.execute(f'''
                SELECT gardenID from GARDEN where gardenName = '{gardenName}'
                ''')
    
    gardenID = cur.fetchall()[0][0]
    
    locationID = identify_location(gardenID, lineID, con)

    cur.execute(f'''
                INSERT INTO USER_LOCATION
                VALUES ({employeeID}, {locationID})
                ''')

    con.commit()
