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
        class Response:
            def __init__(self) -> None:
                self.response = {
                    'message' : 'Server not Found!',
                    'code': '404'
                }
            def json(self) -> dict[str, str]:
                return self.response
            
        response = Response()
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

    >>> item = 
        {
            "user_info" : {
                'user_name' : 'user name',
                'password' : 'password'
            },
            "new_user_info" : {
                'user_name' : 'user name',
                'password' : 'password'
            }
        }
        
    >>> create_new_user(item = item)
    {'message' : '...','code': 'XXX'}
    """

    api_name = '/create-new-user'
    
    response = __request(api_name, item)
    return response

def analyze(item: dict):
    """
    Make a request to database server to analyze.

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

    >>> from PIL import Image
    >>> from encode_decode import encode_image
    >>> image = Image.open('image.JPG')
    >>> encoded_image = encode_image(image)
        >>> item = {
            'user_info' : {
                'user_name' : 'user name',
                'password' : 'password'
            },
            'image_info' : {
                'image' : encoded_image,
                'date' : '12093'
            }
        }
    >>> analyze(item = item)
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
    
    api_name = '/analyze'
    
    response = __request(api_name, item)
    return response

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
    api_name = '/get-history'
    
    response = __request(api_name, item)
    return response


def change_password(item: dict):
    """
    Make a request to database server to check user login.

    Args:
        item: dict[str, str]

    Returns:
        response = {
            'message' : 'message!',
            'code': 'error code!',
        }
        
    Example:

    >>> item = {
            'user_info': {
                'user_name' : 'user name',
                'password' : 'password'
            }
            'new_password': 'new password'
        }
    >>> change_password(item = item)
    {
        'message' : 'message!',
        'code': 'error code!',
    }
    """
    api_name = '/change-password'
    
    response = __request(api_name, item)
    return response

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
    api_name = '/get-statistics'
    
    response = __request(api_name, item)
    return response
    
def get_all_solutions(item: dict):
    """
    Make a request to database server to get all solutions.

    Returns:
        response = dict(key: value)
    Example:
    >>> get_all_solutions()
    {
        'diseaseName' :         tuple(diseaseName), 
        'diseaseCause':         tuple(diseaseCause),
        'diseaseSymptom':       tuple(diseaseSymptom), 
        'solutionPrevention':   tuple(solutionPrevention),
        'solutionGardening':    tuple(solutionGardening),
        'solutionFertilization':tuple(solutionFertilization),
        'solutionSource':       tuple(solutionSource)
    }
    """ 
    api_name = '/get-statistics'
    
    response = __request(api_name, item)
    return response

if __name__ == '__main__':
    from PIL import Image
    from encode_decode import encode_image

    image = Image.open('049230435087359914.JPG')
    encoded_image = encode_image(image)
    print(type(encoded_image))
    item = {
        'user_info' : {
            'user_name' : 'user name',
            'password' : 'password'
        },
        'image_info' : {
            'image' : encoded_image,
            'date' : '12093'
        }
    }
    print(analyze(item).json())