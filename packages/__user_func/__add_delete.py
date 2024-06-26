def add_employee(item: dict, request: object):
    """
    Make a request to database server to create new user.

    Args:
        item: data to request.

    Returns:
        response = {
            'message' : 'message!',
            'code': 'error code!'
        }
        
    Example:

    >>> item = 
        {
            "manager_info" : {
                'user_name' : 'user name',
                'password' : 'password'
            },
            "employee_info" : {
                'user_name' : 'user name',
                'password' : 'password'
            }
        }
        
    >>> add_employee(item = item)
    {'message' : '...','code': 'XXX'}
    """

    api_name = '/add_employee'
    
    response = request(api_name, item)
    return response

def delete_employee(item:dict, request: object):
    """
    Make a request to database server to delete employee infomation.

    Args:
        item: dict[str, str]

    Returns:
        response = dict(key, value)
    Example:
    >>> item = {
        'manager_info': {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'employee_info': {
            'user_name' : 'user name',
            }
    }
    >>> delete_employee(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
        }
    }
    """
    api_name = '/delete_employee'
    response = request(api_name, item)
    return response