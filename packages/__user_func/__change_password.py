def change_password(item: dict):
    """
    Make a request to database server to check user login.

    Args:
        item: dict[str, str]

    Returns:
        response = {
            'message' : 'message!',
            'code': 'error code!',
        }
        
    Example:

    >>> item = {
            'user_info': {
                'user_name' : 'user name',
                'password' : 'password'
            }
            'new_password': 'new password'
        }
    >>> change_password(item = item)
    {
        'message' : 'message!',
        'code': 'error code!'   ,
    }
    """
    api_name = '/change_password'
    
    response = _request(api_name, item)
    return response