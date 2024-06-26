def check_login(item: dict):
    """
    Make a request to database server to check user login.

    Args:
        item: dict[str, str]

    Returns:
        response = {
            'message' : 'message!',
            'code': 'error code!'
        }
        
    Example:

    >>> item = {
            'user_name' : 'user name',
            'password' : 'password'
        }
    >>> check_login(item = item)
    {'message' : '...','code': 'XXX'}
    """
    api_name = '/check_login'
    
    response = _request(api_name, item)
    return response