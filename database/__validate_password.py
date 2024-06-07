from __check_user import check_user
from __check_password import check_password

def validate_password(userName, userPassword, con) -> dict:
    '''
            This private function is used for validating user

            :input:
            userName: str,
            userPassword: str,
            con: sqlite3.connect(<database directory>)

            :return:
            type(bool)
            '''  
    if not check_user(userName, con):
        return {'message':'userName not exist!',
                'code':'003'} 
    else:
        if check_password(userName, userPassword, con):
            return {'message':'Success!',
                    'code':'000'}
        else:
            return {'message':'Wrong password!',
                    'code':'002'}  