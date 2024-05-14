import requests
import dns.resolver

"""
    Contain all request functions for Website.
"""

my_ddns = 'truong51972.ddns.net'
port = 8000

base_url = "http://{}:{}"

def __ddns_to_ip(domain: str) -> str:
    answers = dns.resolver.resolve(domain, 'A')
    return next(iter(answers)).address

def __request(api_name: str, json: dict):
    try:
        ip = __ddns_to_ip(my_ddns)
        url = base_url.format(ip, port) + api_name
        print(f"Sending request to: '{url}'!")
        response = requests.post(url, json= json, timeout=5)
    except:
        response = {
            'message' : 'Server not Found!',
            'code': '404'
        }
    return response

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
    api_name = '/check-login'
    
    response = __request(api_name, item)
    return response

def create_new_user(item: dict):
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

    >>> item = {
            'user_name' : 'user name',
            'password' : 'password'
        }
    >>> create_new_user(item = item)
    {'message' : '...','code': 'XXX'}
    """

    api_name = '//create-new-user'
    
    response = __request(api_name, item)
    return response

def predict(item: dict):
    """
    Make a request to database server to create new user.

    Args:
        item: data to request.

    Returns:
        response = {
            'message' : 'message!',
            'code': 'error code!',
            'result': {
                'class_name' : 'class name',
                'description' : 'description',
                'solution' : 'solution'
            }
        }
        
    Example:

    >>> item = {
            'user_info': {
                'info': {
                    'user_name' : 'user name',
                    'password' : 'password'
                },
            'image_info' : {
                'image' : 'decoded image',
                'date' : 'DD-MM-YYYY'
            }
        }
    >>> predict(item = item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'result': {
            'class_name' : 'class name',
            'description' : 'description',
            'solution' : 'solution'
        }
    }
    """
    
    api_name = '/predict'
    
    response = __request(api_name, item)
    return response

if __name__ == '__main__':
    item = {
        'user_name' : 'user name',
        'password' : 'password'
    }
    print(predict(item))