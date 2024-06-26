def get_management_info(item: dict, request: object):
    """
    Make a request to database server to get all task information of all workers.

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
    >>> get_management_info(item = item)
    {
        "garden_info" : {
            "num_of_garden" : int,
            "line_of_each_garden" : int,    
        },
        "tasks_info" : {
            "Tên" : list,
            "Vườn" : list,
            "Hàng" : list,
            "Số tấm" : list,
        }
    }
    """
    api_name = '/get_management_info'
    
    response = request(api_name, item)
    return response