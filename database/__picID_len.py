import sqlite3

def picID_list_len(con):
    '''
            This private function is used for getting number of pictures saved in database

            :return:
            list_len: int
            '''  
    cur = con.cursor()

    cur.execute(f"""
            SELECT picID FROM PIC
            """)

    picID_list = cur.fetchall()
    list_len = len(picID_list)

    con.commit()

    return list_len