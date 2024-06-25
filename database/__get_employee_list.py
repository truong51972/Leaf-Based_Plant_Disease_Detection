import sqlite3

def get_employee(managerName:str, 
                 con):
    cur = con.cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    managerID = cur.fetchall()[0][0]

    cur.execute(f'''
                SELECT e.userID AS employeeID, e.userName AS employeeName
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {managerID}
                ''')
    
    employee_list = cur.fetchall()
    employeeID_list = list(map(lambda x: x[0], employee_list))
    employeeName_list = list(map(lambda x: x[1], employee_list))

    return employeeID_list, employeeName_list