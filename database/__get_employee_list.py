import sqlite3

def get_employee(managerName:str, 
                      con):
    cur = con.cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{managerName}'
        ''')
    
    userID = cur.fetchall()[0][0]

    cur.execute(f'''
                SELECT e.userID AS employeeID
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {userID}
                ''')
    
    employee_list = cur.fetchall()
    employee_list = list(map(lambda x: x[0], employee_list))

    return employee_list