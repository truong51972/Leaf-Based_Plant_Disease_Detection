import sqlite3

def picID_list_len(database='data.db'):
    '''
            This private function is used for getting number of pictures saved in database

            :return:
            list_len: int
            '''  
    con = sqlite3.connect(database)
    cur = con.cursor()

    cur.execute(f"""
            SELECT picID FROM PIC
            """)

    picID_list = cur.fetchall()
    list_len = len(picID_list)

    con.commit()

    return list_len