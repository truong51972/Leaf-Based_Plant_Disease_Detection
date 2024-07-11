def get_statistics(item: dict, request: object):
    """
    Make a request to database server to get statistics.

    Args:
        item: dict[str, str]

    Returns:
        response = dict(key: value)
    Example:
    >>> item = {
        'user_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'start_date': 'YYYY-MM-DD',
        'end_date': 'YYYY-MM-DD',
        'garden_name': str
    }
    >>> get_statistics(item = item)
    {
        'overall_data' : dict(key, value),
        'per_line' : {
            'Hàng 1' : {
                'Khoẻ' : int,
                'Bệnh' : int,
                'Chi tiết' : {
                    dict('Tên bệnh' : số lượng)
                }
            },
            'Hàng 2' : {
                'Khoẻ' : int,
                'Bệnh' : int,
                'Chi tiết' : {
                    dict('Tên bệnh' : số lượng)
                }
            }
        }
    }
    """
    api_name = '/get_statistics'
    
    response = request(api_name, item)
    return response
    
