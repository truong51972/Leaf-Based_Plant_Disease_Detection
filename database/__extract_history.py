import sqlite3
from .__check_manager import is_manager

def extract_history(userName, is_over_threshold, con):
    '''
        :return:
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        score,
        threshold,
        lineID,
        gardenName,
        plantName)
        '''

    cur = con.cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{userName}'
        ''')
    
    userID = cur.fetchall()[0][0]

    con.commit()

    if is_over_threshold:
        if is_manager(userName, con):
            cur = con.cursor()
            cur.execute(f'''
            select userID, 
                PIC.pic, 
                PIC.picDate, 
                DISEASE.diseaseName,
                PIC.pred_pic,
                PIC.score,
                PIC.threshold,
                LOCATION.lineID,
                GARDEN.gardenName,
                GARDEN.plantName         
            from USER_PIC
            join PIC on USER_PIC.picID = PIC.picID
            join DISEASE on PIC.diseaseID=DISEASE.diseaseID
            join LOCATION on LOCATION.locationID = PIC.locationID
            join GARDEN on LOCATION.gardenID = GARDEN.gardenID
            where userID = {userID} or userID in (
                SELECT e.userID AS employeeID
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {userID})
                and PIC.score > PIC.threshold
            order by picDate desc          
            ''')
            
        else:
            cur = con.cursor()
            cur.execute(f'''
            select userID, 
                PIC.pic, 
                PIC.picDate, 
                DISEASE.diseaseName,
                PIC.pred_pic,
                PIC.score,
                PIC.threshold,
                LOCATION.lineID,
                GARDEN.gardenName,
                GARDEN.plantName         
            from USER_PIC
            join PIC on USER_PIC.picID = PIC.picID
            join DISEASE on PIC.diseaseID=DISEASE.diseaseID
            join LOCATION on LOCATION.locationID = PIC.locationID
            join GARDEN on LOCATION.gardenID = GARDEN.gardenID
            where userID = {userID} and PIC.score > PIC.threshold
            order by picDate desc          
            ''')
    else:
        if is_manager(userName, con):
            cur = con.cursor()
            cur.execute(f'''
            select userID, 
                PIC.pic, 
                PIC.picDate, 
                DISEASE.diseaseName,
                PIC.pred_pic,
                PIC.score,
                PIC.threshold,
                LOCATION.lineID,
                GARDEN.gardenName,
                GARDEN.plantName         
            from USER_PIC
            join PIC on USER_PIC.picID = PIC.picID
            join DISEASE on PIC.diseaseID=DISEASE.diseaseID
            join LOCATION on LOCATION.locationID = PIC.locationID
            join GARDEN on LOCATION.gardenID = GARDEN.gardenID
            where userID = {userID} or userID in (
                SELECT e.userID AS employeeID
                FROM USER e
                inner JOIN USER m ON e.managerID = m.userID
                where m.userID = {userID})
                and PIC.score < PIC.threshold
            order by picDate desc          
            ''')
            
        else:
            cur = con.cursor()
            cur.execute(f'''
            select userID, 
                PIC.pic, 
                PIC.picDate, 
                DISEASE.diseaseName,
                PIC.pred_pic,
                PIC.score,
                PIC.threshold,
                LOCATION.lineID,
                GARDEN.gardenName,
                GARDEN.plantName         
            from USER_PIC
            join PIC on USER_PIC.picID = PIC.picID
            join DISEASE on PIC.diseaseID=DISEASE.diseaseID
            join LOCATION on LOCATION.locationID = PIC.locationID
            join GARDEN on LOCATION.gardenID = GARDEN.gardenID
            where userID = {userID} and PIC.score < PIC.threshold
            order by picDate desc          
            ''')


    history = cur.fetchall()
    con.commit()    

    pic = list(map(lambda x: x[1], history))
    picDate = list(map(lambda x: x[2], history))
    class_name = list(map(lambda x: x[3], history))
    pred_pic = list(map(lambda x: x[4], history))
    score = list(map(lambda x: x[5], history))
    threshold = list(map(lambda x: x[6], history))
    lineID = list(map(lambda x: x[7], history))
    gardenName = list(map(lambda x: x[8], history))
    plantName = list(map(lambda x: x[9], history))

    return (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        score,
        threshold,
        lineID,
        gardenName,
        plantName)