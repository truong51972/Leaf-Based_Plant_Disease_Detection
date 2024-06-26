def task_employee(item: dict, request: object):
    """
    Make a request to database server to give task for employee.

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
        'garden_name': str
    }
    >>> task_employee(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'table':{
        "Tên nhân viên: [str]
        "Hàng:[str]}
        }
    }
    """
    api_name = '/task_employee'
    response = request(api_name, item)
    return response