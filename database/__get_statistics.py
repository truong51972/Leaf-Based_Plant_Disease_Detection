import sqlite3
from copy import deepcopy
from .__check_manager import is_manager

def get_statistic(userName, con=sqlite3.connect('data.db')):

    cur = con.cursor()

    cur.execute(f'''
                select diseaseName from DISEASE
            ''')

    disease_list = cur.fetchall()
    disease_list = list(map(lambda x: x[0], disease_list))
    disease_count = dict().fromkeys(disease_list,0)

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{userName}'
        ''')
    
    userID = cur.fetchall()[0][0]

    con.commit()

    if is_manager(userName, con):
        print('manager mode')
        cur.execute(f'''
            select sum(num_count) as count, diseaseName, date from
            (select count(*) as [num_count], DISEASE.diseaseName, date(PIC.picDate) as date, USER.userID
            from PIC join DISEASE on PIC.diseaseID = DISEASE.diseaseID
            join USER_PIC on PIC.picID = USER_PIC.picID
            join USER on USER_PIC.userID = USER.userID
            where USER.userID = {userID} or USER.userID in (
                SELECT e.userID AS employeeID
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {userID})
            group by date(picDate), PIC.diseaseID, USER.userID)
            group by diseaseName, date
            order by date
        ''')
    else:
        print('employee mode')
        print(f'userID = {userID}')
        cur.execute(f'''select count(*) as [num_count], DISEASE.diseaseName, date(PIC.picDate), USER.userID
                        from PIC join DISEASE on PIC.diseaseID = DISEASE.diseaseID
                        join USER_PIC on PIC.picID = USER_PIC.picID
                        join USER on USER_PIC.userID = USER.userID
                        where USER.userID = {userID}
                        group by date(picDate), PIC.diseaseID, USER.userID''')
        
    data = cur.fetchall()
    list_date = list(map(lambda x: x[2], data))
    set_date = set(list_date)

    statistics = dict()

    for i in set_date:
        statistics[i] = deepcopy(disease_count)

    for data_batch in data:
        statistics[data_batch[2]].update({data_batch[1]: data_batch[0]})

    return statistics