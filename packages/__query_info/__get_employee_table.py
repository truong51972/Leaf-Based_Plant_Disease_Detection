def get_location_assignment_table(item: dict, request: object):
    """
    Make a request to database server to get all tasks of employee.

    Args:
        item: dict[str, str]

    Returns:
        response = dict(key, value)
    Example:
    >>> from ... import _request

    >>> item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'garden_name': str
    }
    >>> get_location_assignment_table(item=item, request= _request)
    {
        'message' : 'message!',
        'code': 'error code!',
        'table':{
            "Tên nhân viên: [str],
            "Hàng 1: [bool],
            "Hàng 2: [bool],
            ...
            "Hàng n: [bool],
        }
    }
    """
    api_name = '/get_location_assignment_table'
    response = request(api_name, item)
    return response