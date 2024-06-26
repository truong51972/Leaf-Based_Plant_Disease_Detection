def delete_garden(item:dict, request: object):
    """
    Make a request to database server to delete garden infomation.

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
    >>> delete_garden(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
        }
    }
    """
    api_name = '/delete_garden'
    response = request(api_name, item)
    return response

def add_garden(item: dict, request: object):
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
        'garden_info' : {
            'plant_name' : str,
            'garden_name' : str,
            'num_of_line' : int
        }
    }
    >>> add_garden(item = item)
    {
        'message' : 'message!',
        'code': 'error code!',
    }
    """
    api_name = '/add_garden'
    
    response = request(api_name, item)
    return response