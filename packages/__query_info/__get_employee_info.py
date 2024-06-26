def get_employee_info(item:dict):
    """
    Make a request to database server to get employer infomation.

    Args:
        item: dict[str, str]

    Returns:
        response = dict(key, value)
    Example:
    >>> item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
    }
    >>> get_employee_info(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'employee_info' :{
            'ID: [int],
            'Tên nhân viên': [str] 
        }
    }
    """
    api_name = '/get_employee_info'
    response = _request(api_name, item)
    return response