import sqlite3
from copy import deepcopy
import pandas as pd

def __del_location(gardenName:str, 
                   con):
    cur = con.cursor()
    cur.execute(f'''
                delete from USER_LOCATION
                where USER_LOCATION.locationID in (
                    select LOCATION.locationID
                    from LOCATION join GARDEN on LOCATION.gardenID = GARDEN.gardenID
                    where GARDEN.gardenName = '{gardenName}'
                )
                ''')
    
    con.commit()

def create_table(gardenName:str,
                 managerName:int,
                 con):
    
    '''
        :output:
        dict = {
            'message': str,
            'code': str,
            'table': {
                "Tên Nhân Viên": ['employeeName1', 'employeeName2', ...],
                "Hàng 1": [bool, bool, ...],
                "Hàng 2": [bool, bool, ...],
                ...
                }
        }
        '''
    cur = con.cursor()

    cur.execute(f'''
        SELECT gardenID 
        FROM GARDEN
        WHERE gardenName = '{gardenName}'
        ''')
    
    gardenID = cur.fetchall()[0][0]

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    managerID = cur.fetchall()[0][0]

    cur.execute(f'''
                select LOCATION.lineID from LOCATION where LOCATION.gardenID = {gardenID}
                ''')
    
    lineID_list = list(map(lambda x: 'Hàng ' + str(x[0]), cur.fetchall()))

    cur.execute(f'''
                SELECT e.userName AS employeeName, e.userID as employeeID
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {managerID}
                ''')
    
    employeeName_list = list(map(lambda x: x[0], cur.fetchall()))
    employeeID_list = list(map(lambda x: x[1], cur.fetchall()))

    table = {
        'Tên Nhân Viên': employeeName_list
    }

    cur.execute(f'''
                SELECT userName, lineID
                FROM USER_LOCATION
                JOIN LOCATION on USER_LOCATION.locationID = LOCATION.locationID
                JOIN USER on USER_LOCATION.userID = USER.userID
                WHERE gardenID = {gardenID}
                ''')
    
    assigned_line = cur.fetchall() # test_emp1	3   test_emp2	1   test_emp2	4    emp	2

    for i in lineID_list:
        # i = 'hang 1', ...
        bool_list = [False]*len(employeeName_list)
        table.update({i : deepcopy(bool_list)})

    for i in assigned_line:
        userName, lineID = i[0], i[1]
        lineName = 'Hàng ' + str(lineID)
        index = employeeName_list.index(userName)
        table[lineName][index] = True
    
    return table

def insert_assignment_table(gardenName:str,
                            table:pd.DataFrame,
                            con):
    def combine_names(col_row):
        col, row = col_row
        return col[1], row
    
    def convert_result(result, gardenID):
        final = []
        for i, j in result:
            if type(j) == str:
                employeeName = j
                cur.execute(f'''
                            SELECT userID 
                            FROM USER
                            WHERE userName = '{employeeName}'
                            ''')
                employeeID = cur.fetchall()[0][0]
            else:
                lineID = int(i[5:])
                cur.execute(f'''
                            SELECT LOCATION.locationID
                            FROM LOCATION
                            WHERE gardenID = {gardenID} and lineID = {lineID}
                            ''')
                final_lineID = cur.fetchall()[0][0]
                final.append((employeeID, final_lineID))
        return final

    cur = con.cursor()
    cur.execute(f'''
                SELECT gardenID 
                FROM GARDEN
                WHERE gardenName = '{gardenName}'
                ''')
    gardenID = cur.fetchall()[0][0]

    result = list(map(combine_names, filter(lambda x: x[1], table.stack().items())))
    
    final = convert_result(result, gardenID)

    __del_location(gardenName, con)

    for i in final:
        cur.execute(f'''
                    INSERT INTO USER_LOCATION 
                    VALUES ({i[0]}, {i[1]})      
                    ''')
        
        con.commit()


    
