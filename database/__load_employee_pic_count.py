import sqlite3

def load_employee_pic_count(managerName:str, 
                            con):
    cur = con. cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    managerID = cur.fetchall()[0][0]

    cur.execute(f'''
                SELECT userName, gardenName, lineID, count(*) as pic_count FROM
                (SELECT USER.userName as userName, GARDEN.gardenName as gardenName, LOCATION.lineID as lineID
                FROM USER
                RIGHT JOIN USER_LOCATION ON USER.userID = USER_LOCATION.userID
                JOIN USER_PIC ON USER_PIC.userID = USER.userID
                JOIN PIC ON PIC.picID = USER_PIC.picID
                JOIN LOCATION on PIC.locationID = LOCATION.locationID
                JOIN GARDEN on LOCATION.gardenNum = GARDEN.gardenID
                WHERE USER.userID in (SELECT e.userID AS employeeID
                                    FROM USER e
                                    INNER JOIN USER m ON e.managerID = m.userID
                                    WHERE m.userID = {managerID})
                GROUP BY USER.userID, USER_LOCATION.userID, USER_PIC.userID, PIC.picID)
                GROUP BY userName, gardenName, lineID
                ''')
    
    data = cur.fetchall()

    employeeName = list(map(lambda x: x[0], data))
    gardenName = list(map(lambda x: x[1], data))
    lineID = list(map(lambda x: x[2], data))
    picCount = list(map(lambda x: x[3], data))

    return (employeeName, gardenName, lineID, picCount)
    
