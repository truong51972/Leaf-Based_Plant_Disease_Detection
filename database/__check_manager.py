import sqlite3

def is_manager(userName, con=sqlite3.connect('data.db')):
    cur = con.cursor()

    cur.execute(f'''
            SELECT managerID FROM USER WHERE userName = '{userName}'
        ''')
    
    status = cur.fetchall()[0][0]

    if status is None:
        return True
    else:
        return False