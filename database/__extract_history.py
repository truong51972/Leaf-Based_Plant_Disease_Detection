import sqlite3
from .__check_manager import is_manager

def extract_history(userData, con):
    '''
        :return:
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        score)
        '''
    userName = userData.user_name

    cur = con.cursor()

    cur.execute(f'''
        SELECT userID 
        FROM USER
        WHERE userName = '{userName}'
        ''')
    
    userID = cur.fetchall()[0][0]

    con.commit()

    if is_manager(userName, con):
        cur = con.cursor()
        cur.execute(f'''
        select userID, 
                pic, 
                picDate, 
                diseaseName,
                pred_pic,
                score
        from USER_PIC
        join PIC on USER_PIC.picID = PIC.picID
        join DISEASE on PIC.diseaseID=DISEASE.diseaseID
        where userID = {userID} or userID in (
            SELECT e.userID AS employeeID
            FROM USER e
            inner JOIN USER m ON e.managerID = m.userID
            where m.userID = {userID})
        order by picDate desc          
        ''')

        history = cur.fetchall()
        con.commit()
        
    else:
        cur = con.cursor()
        cur.execute(f'''
        select userID, 
                pic, 
                picDate, 
                diseaseName,
                pred_pic,
                score
        from USER_PIC
        join PIC on USER_PIC.picID = PIC.picID
        join DISEASE on PIC.diseaseID=DISEASE.diseaseID
        where userID = {userID}
        order by picDate desc          
        ''')
        history = cur.fetchall()
        con.commit()
        
    pic = list(map(lambda x: x[1], history))
    picDate = list(map(lambda x: x[2], history))
    class_name = list(map(lambda x: x[3], history))
    pred_pic = list(map(lambda x: x[4], history))
    score = list(map(lambda x: x[5], history))

    return (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        score)