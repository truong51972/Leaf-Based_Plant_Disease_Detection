import sqlite3

def del_employee(employeeName:str,
                 con):
    
    cur = con.cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{employeeName}'
        ''')
    
    employeeID = cur.fetchall()[0][0]

    cur.execute(f'''
                delete from USER_PIC
                where USER_PIC.userID = {employeeID}
                ''')
    
    con.commit()

    cur.execute(f'''
                delete from USER_LOCATION
                where USER_LOCATION.userID = {employeeID}
                ''')
    
    con.commit()

    cur.execute(f'''
                delete from USER
                where USER.userID = {employeeID}
                ''')
    
    con.commit()
