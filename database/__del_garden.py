import sqlite3

def del_garden(
               gardenName: str,
               con):
    
    cur = con.cursor()

    cur.execute(f'''
        SELECT gardenID 
        FROM GARDEN
        WHERE gardenName = '{gardenName}'
        ''')
    
    gardenID = cur.fetchall()[0][0]

    cur.execute(f'''
                delete from USER_LOCATION
                where USER_LOCATION.locationID in (
                    select locationID 
                    from LOCATION
                    where LOCATION.gardenID = {gardenID}
                )
                ''')
    
    con.commit()

    cur.execute(f'''
                delete from USER_PIC
                where USER_PIC.picID in (
                    select picID 
                    from PIC
                    where PIC.locationID in (
                        select locationID 
                        from LOCATION
                        where LOCATION.gardenID = {gardenID}
                )
                )
                ''')
    
    con.commit()

    cur.execute(f'''
                delete from PIC
                where PIC.locationID in (
                    select locationID 
                    from LOCATION
                    where LOCATION.gardenID = {gardenID}
                )
                ''')
    
    con.commit()

    cur.execute(f'''
                DELETE FROM LOCATION
                WHERE gardenID = {gardenID}
                ''')
    
    con.commit()

    cur.execute(f'''
                DELETE FROM GARDEN
                WHERE gardenID = {gardenID}
                ''')
    
    con.commit()