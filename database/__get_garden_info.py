import sqlite3
from copy import deepcopy

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

def garden_info_employee(employeeName:str,
                         con):
    
    cur = con.cursor()
    
    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{employeeName}'
        ''')
    
    employeeID = cur.fetchall()[0][0]

    cur.execute(f'''
        select GARDEN.gardenName, LOCATION.lineID, GARDEN.plantName
        from LOCATION 
        join USER_LOCATION on LOCATION.locationID = USER_LOCATION.locationID
        join USER on USER_LOCATION.userID = USER.userID
        join GARDEN on GARDEN.gardenID = LOCATION.gardenID
        where USER.userID = {employeeID}
        ''')
    
    data = cur.fetchall()

    gardenName_list = set(map(lambda x: x[0], data))

    final = dict()

    info_dict = {
        'Luống': list(),
        'Giống cây': None
    }

    for i in gardenName_list:
        final.update({i : deepcopy(info_dict)})

    for i in data:
        gardenName, lineName, plantName = i[0], 'Hàng ' + str(i[1]), i[2]
        final[gardenName]['Luống'].append(lineName)
        if final[gardenName]['Giống cây'] is None:
            final[gardenName]['Giống cây'] = plantName

    return final