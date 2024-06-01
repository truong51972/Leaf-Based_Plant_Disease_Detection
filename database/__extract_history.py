import sqlite3

def extract_history(userData, con):
    '''
        :return:
        (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob)
        '''
    userName = userData.user_name

    if userName == 'admin':
        cur = con.cursor()
        cur.execute(f'''
        select userName, 
                pic, 
                picDate, 
                diseaseName,
                pred_pic,
                class_prob
        from USER_PIC
        join PIC on USER_PIC.picID = PIC.picID
        join DISEASE on PIC.class_name=DISEASE.class_name
        order by picDate desc           
        ''')

        history = cur.fetchall()
        con.commit()
        
    else:
        cur = con.cursor()
        cur.execute(f'''
        select userName, 
                pic, 
                picDate, 
                diseaseName,
                pred_pic,
                class_prob
        from USER_PIC
        join PIC on USER_PIC.picID = PIC.picID
        join DISEASE on PIC.class_name=DISEASE.class_name
        where userName = '{userName}'
        order by picDate desc           
        ''')
        history = cur.fetchall()
        con.commit()
        
    pic = [i[1] for i in history]
    picDate = [i[2] for i in history]
    class_name = [i[3] for i in history]
    pred_pic = [i[4] for i in history]
    class_prob = [i[5] for i in history]

    return (pic, 
        picDate, 
        class_name, 
        pred_pic, 
        class_prob)