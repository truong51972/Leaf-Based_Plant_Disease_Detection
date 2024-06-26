def get_history(item: dict):
    """
    Make a request to database server to check user login.

    Args:
        item: dict[str, str]

    Returns:
        response = {
            'message' : 'message!',
            'code': 'error code!',
            'history': {
                'Ảnh gốc': [...],
                'Ảnh phân tích': [...],
                'Tên bệnh': [...]
                'Độ tin cây': [...],
                'Ngày chụp': [...]
            }
        }
        
    Example:

    >>> item = {
            'user_name' : 'user name',
            'password' : 'password'
        }
    >>> get_history(item = item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'history': {
            'Ảnh gốc': [...],
            'Ảnh phân tích': [...],
            'Tên bệnh': [...]
            'Độ tin cây': [...],
            'Ngày chụp': [...]
        }
    }
    """
    api_name = '/get_history'
    
    response = _request(api_name, item)
    return response