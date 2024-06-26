def get_gardens_info(item: dict):
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
    >>> get_gardens_info(item = item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'garden_info' : {
            'Tên vườn' : [str],
            'Tên loại cây' : [str],
            'Số luống' : [int]
        }
    }
    """
    api_name = '/get_gardens_info'
    response = _request(api_name, item)
    return response