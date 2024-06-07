from __check_user import check_user
from __check_password import check_password
from __add_user import add_user
from __picID_len import picID_list_len
from __extract_history import extract_history
def main():
    import sqlite3
    from datetime import datetime
    import pytz
    def is_password_correct(userName:str, userPassword:str) -> bool:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
            SELECT userPassword from USER WHERE userName = '{userName}'
        """)    
        password = cur.fetchone()
        
        con.commit()
        con.close()

        if userPassword == password[0]:
            return True
        else:
            return False
        
    def is_exist_user(userName:str) -> bool:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f"""
        SELECT userName from USER  
        """)    
        user = cur.fetchone()
        con.commit()
        con.close() 
        if userName in user:
            return True
        else:
            return False
        
    def validate_password(userName, userPassword) -> dict:
        if not is_exist_user(userName):
            return {'message':'userName not exist!',
                    'code':'003'} 
        else:
            if is_password_correct(userName, userPassword):
                return {'message':'Success!',
                        'code':'000'}
            else:
                return {'message':'Wrong password!',
                        'code':'002'}  
        
    def user_login(userData) -> dict:
        '''
            PERFORMANCE CODE:
                '000': Action proceeded successfully 
                '002': userPassword doesn't match with the userName in the database (WrongPassword)
                '003': userName doesn't exist in the database (UserNotFound)
        '''

        userName = userData.user_name
        userPassword = userData.password

        print(userName, userPassword)

    def add_picture_to_database(picID, diseaseID, picDate, pic, pred_pic, pred_accuracy):

        # Định dạng thời gian theo YYYY-MM-DD HH:MI:SS
        formatted_time = picDate.strftime('%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        con = sqlite3.connect('data.db')
        cur = con.cursor()

        cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, {diseaseID}, '{formatted_time}', '{pic}', '{pred_pic}', {pred_accuracy}) 
        """)

        con.commit()
        con.close()

    def bruh(item):   
        '''
    :input:
    item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'image_info' : {
            'image' : 'decoded image',
            'date' : 'YYYY-MM-DD HH:MI:SS',
            'class_name': None,
            'accuracy': None,
            'predicted_image': None
        }
    }

    :return:
    {
    'message' : 'message!',
    'code': 'error code!',
    'result': {
        'class_name' : 'class name' or None,
        'description' : (type = dictionary) or None,
        'solution' : (type = dictionary) or None
    }
    }'''     
        def __picID_list_len():
            con = sqlite3.connect('data.db')
            cur = con.cursor()

            cur.execute(f"""
            SELECT picID FROM PIC
            """)

            picID_list = cur.fetchall()
            list_len = len(picID_list)

            con.commit()
            con.close()

            return list_len
        
        def __extract_result(picID:int):    
            con = sqlite3.connect('data.db')
            cur = con.cursor()

            cur.execute(f"""
            select picID,
                   diseaseName, 
                   diseaseCause, 
                   diseaseSymptom, 
                   solutionPreventation,
                   solutionGardening,
                   solutionFertilization,
                   solutionSource
            from
            (
            select * from 
            (
                PIC join DISEASE on PIC.diseaseID=DISEASE.diseaseID
            )
                join SOLUTION on SOLUTION.diseaseID=PIC.diseaseID
            )
            """)

            data_list = cur.fetchall()[0]
            (diseaseName, 
             diseaseCause,
             diseaseSymptom, 
             solutionPreventation,
             solutionGardening,
             solutionFertilization,
             solutionSource) = (
                 data_list[1],
                 data_list[2],
                 data_list[3],
                 data_list[4],
                 data_list[5],
                 data_list[6],
                 data_list[7]
                 ) 
            
            class_name = diseaseName
            description = {
                'cause':diseaseCause,
                'symptom':diseaseSymptom                
            }
            solution = {
                'prevention':solutionPreventation,
                'gardening':solutionGardening,
                'fertilization':solutionFertilization,
                'source':solutionSource
            }

            con.commit()
            con.close()

            return class_name, description, solution

            # return class_name, description, solution
               

        userName = item['user_info']['user_name']
        userPassword = item['user_info']['password']

        validate_result = validate_password(userName, userPassword)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'result': {
                    'class_name' : None,
                    'description' : None,
                    'solution' : None
                        }
                    }

        pred_pic = item['image_info']['predicted_image']
        pred_acc = item['image_info']['accuracy']
        pic = item['image_info']['image']
        picDate = item['image_info']['date']
        diseaseID = item['image_info']['class_name']
        picID = __picID_list_len()

        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f'''
        INSERT INTO USER_PIC VALUES ('{userName}', {picID})
        ''')
        con.commit()
        con.close()

        add_picture_to_database(picID, diseaseID, picDate, pic, pred_pic, pred_acc)
        class_name, description, solution = __extract_result(picID)
        return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'result': {
                    'class_name' : class_name,
                    'description' : description,
                    'solution' : solution
                          }
                }
    
    def __get_history(userData):

        userName = userData['user_info']['user_name']
        userPassword = userData['user_info']['password']

        def validate_password(userName, userPassword) -> dict:
            if not is_exist_user(userName):
                return {'message':'userName not exist!',
                     'code':'003'} 
            else:
                if is_password_correct(userName, userPassword):
                    return {'message':'Success!',
                           'code':'000'}
                else:
                    return {'message':'Wrong password!',
                           'code':'002'} 

        validate_result = validate_password(userName, userPassword)
        if validate_result['code'] == '002' or validate_result['code'] == '003':
            return {
                'message' : validate_result['message'],
                'code': validate_result['code'],
                'result': {
                    'class_name' : None,
                    'description' : None,
                    'solution' : None
                        }
                    }
        
        con = sqlite3.connect('data.db')
        cur = con.cursor()    

        if userName == 'admin':
            
            cur.execute(f'''
            select * from PIC
            order by picDate desc
            ''')

            history = cur.fetchall()

            return history
        
        else:
            cur.execute(f'''
            select PIC.picID from 
            ( 
            USER_PIC join PIC on PIC.picID=USER_PIC.picID
            )
            ''')

            picID_list = cur.fetchall()
            final_picID_list = tuple(i[0] for i in picID_list)

            con.commit()
    
    def __picID_list_len():
            '''
            This private function is used for getting number of pictures saved in database

            :return:
            list_len: int
            '''  
            con = sqlite3.connect('data.db')
            cur = con.cursor()

            cur.execute(f"""
            SELECT picID FROM PIC
            """)

            picID_list = cur.fetchall()
            list_len = len(picID_list)
            print(picID_list)
            con.commit()

            return list_len
    
    def __add_picture_to_database(picID=3, class_name='Tomato_mosaic_virus', picDate='2024-05-18 17:50:17', pic='adwadw', pred_pic='awdad', class_prob=0.3):
        '''
        This private function is used for adding picture information to database
        :input:
        picID: int,
        class_name: int,
        picDate: datetime (YYYY-MM-DD HH:MI:SS)
        pic: str (enscripted content of the pic)
        '''

        con = sqlite3.connect('data.db')
        cur = con.cursor()
        # formatted time: YYYY-MM-DD HH:MI:SS
        formatted_time = datetime.strptime(picDate, '%Y-%m-%d %H:%M:%S')

        print(formatted_time)

        cur.execute(f"""
        INSERT INTO PIC VALUES ({picID}, '{class_name}', '{formatted_time}', '{pic}', '{pred_pic}', {class_prob}) 
        """)

        con.commit()
    
    # class User:
    #     def __init__(self) -> None:
    #         self.user_name = 'admin'
    #         self.password = 'xW2PqVk-e29mqX3T2aZAYPuBl5e4SKVeKDXfvU9XC9g='

    # user = User()

    # con1 = sqlite3.connect('data.db')
    # con2 = sqlite3.connect('data.db')

    # check_user(user, con1)
    # check_user(user, con2)
    

if __name__ == '__main__':
    import sqlite3
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    cur.execute(f'''
            SELECT picID FROM USER_PIC WHERE userName = 'lol' ORDER BY picID ASC LIMIT 1
        ''')
    
    deleted_id = cur.fetchall()[0][0]

    con.commit()

    cur.execute(f'''
        DELETE FROM USER_PIC 
        WHERE picID = {deleted_id}
        ''')
    con.commit()

    cur.execute(f'''
        DELETE FROM PIC 
        WHERE picID = {deleted_id}
        ''')
    con.commit()

    cur.execute(f'''
        UPDATE PIC 
        SET picID = picID - 1 
        WHERE picID > {deleted_id} 
        ''')
    
    con.commit()

    cur.execute(f'''
        UPDATE USER_PIC 
        SET picID = picID - 1 
        WHERE picID > {deleted_id} 
        ''')
    
    con.commit()
    con.close()
