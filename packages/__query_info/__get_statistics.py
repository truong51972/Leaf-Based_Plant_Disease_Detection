def get_statistics(item: dict):
    """
    Make a request to database server to get statistics.

    Args:
        item: dict[str, str]

    Returns:
        response = dict('ten ben' : so luong, ...)
    Example:
    >>> item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'date': 'YYYY-MM-DD',
        'gardenNum': int,
        'lineNum': int
    }
    >>> get_statistics(item = item)
    {
        'Virus khảm cà chua ToMV': int = ..., 
        'Bệnh bạc lá sớm': int = ..., 
        'Virus TYLCV (Tomato yellow leaf curl virus)': int = ..., 
        'Bệnh tàn rụi muộn': int = ..., 
        'Đốm vi khuẩn': int = ..., 
        'Nấm Corynespora': int = ..., 
        'Nấm Septoria lycopersici': int = ..., 
        'Cây tốt': int = ..., 
        'Bệnh khuôn lá': int = ..., 
        'Bệnh nhện đỏ': int = ...
    }
    """
    api_name = '/get_statistics'
    
    response = _request(api_name, item)
    return response
    
