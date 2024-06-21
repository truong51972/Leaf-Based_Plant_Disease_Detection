import sqlite3
from copy import deepcopy
from .__check_manager import is_manager

def get_statistic(userName:str,
                  date:str,
                  gardenNum:str,
                  lineNum:str, 
                  con):
    '''
    :input:
    userName:str,
    date:str,
    gardenNum:str,
    lineNum:str, 
    con = sqlite3.connect(<database directory>)

    :output:
    statistic = {'Virus khảm cà chua ToMV': int = ..., 
                 'Bệnh bạc lá sớm': int = ..., 
                 'Virus TYLCV (Tomato yellow leaf curl virus)': int = ..., 
                 'Bệnh tàn rụi muộn': int = ..., 
                 'Đốm vi khuẩn': int = ..., 
                 'Nấm Corynespora': int = ..., 
                 'Nấm Septoria lycopersici': int = ..., 
                 'Cây tốt': int = ..., 
                 'Bệnh khuôn lá': int = ..., 
                 'Bệnh nhện đỏ': int = ...}
    '''

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
        cur.execute(f'''
            select count(*) as count, DISEASE.diseaseName, date(PIC.picDate) as date, gardenNum, lineNum
            from PIC join DISEASE on PIC.diseaseID = DISEASE.diseaseID
            join USER_PIC on PIC.picID = USER_PIC.picID
            join USER on USER_PIC.userID = USER.userID
            join LOCATION on PIC.locationID = LOCATION.locationID
            where USER.userID = {userID} or USER.userID in (
                SELECT e.userID AS employeeID
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {userID})
            and date = '{date}' and gardenNum = {gardenNum} and lineNum = {lineNum}
            group by PIC.diseaseID, PIC.locationID
            order by date
        ''')
    else:
        cur.execute(f'''select count(*) as count, DISEASE.diseaseName, date(PIC.picDate) as date, gardenNum, lineNum 
                        from PIC join DISEASE on PIC.diseaseID = DISEASE.diseaseID
                        join USER_LOCATION on PIC.locationID = USER_LOCATION.locationID
                        join USER on USER_LOCATION.userID = USER.userID
                        join LOCATION on PIC.locationID = LOCATION.locationID
                        where USER.userID = {userID} and gardenNum = {gardenNum} and lineNum = {lineNum} and date = '{date}'
                        group by PIC.diseaseID, date, gardenNum, lineNum''')
        
    data = cur.fetchall()

    statistic = deepcopy(disease_count)
  
    for data_batch in data:
        statistic.update({data_batch[1]: data_batch[0]})

    return statistic