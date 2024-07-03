def assign_employee_location(item: dict, request: object):
    """
    Make a request to database server to assign task for employees.

    Args:
        item: dict[str, str]

    Returns:
        response = dict(key, value)
    Example:
    >>> from packages import request_api
    >>> import pandas as pd
    >>> 
    >>> item = {
        'user_info' : {
            'user_name' : str,
            'password' : str,
        }
        'garden_name' : str
    }
    >>> result = request_api.get_location_assignment_table(item).json()
    >>> table = result.table
    >>> 
    >>> df = pd.DataFrame(table)
    >>>
    >>> table = df.to_list()
    >>> table
    {
        'Tên nhân viên' : list(str),
        'Hàng 1' : list(bool),
        'Hàng 2' : list(bool),
        ...
    }
    >>>
    >>> item = {
        'user_info': {
            'user_name' : str = 'user name',
            'password' : str = 'password'
        },
        'table' : dict = table,
        'garden_name': str
    }
    >>> assign_employee_location(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
    }

    PERFORMANCE CODE:
        '000': Action proceeded successfully
        '003': userName doesn't exist in the database (UserNotFound)
        '101': Employee has already been assigned in the selected location (EmployeeLocationExisted)
    """
    api_name = '/assign_employee_location'
    response = request(api_name, item)
    return response