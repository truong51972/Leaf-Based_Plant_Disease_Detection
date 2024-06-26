from .__request import _request

from .__garden_func.__add_delete import add_garden, delete_garden

from .__query_info.__get_all_solutions import get_all_solutions
from .__query_info.__get_employee_info import get_employee_info
from .__query_info.__get_gardens_info import get_gardens_info
from .__query_info.__get_management_info import get_management_info
from .__query_info.__get_history import get_history
from .__query_info.__get_statistics import get_statistics

from .__user_func.__add_delete import add_employee, delete_employee
from .__user_func.__change_password import change_password
from .__user_func.__check_login import check_login
from .__user_func.__task_employee import task_employee

from .__analyze import analyze
"""
    Contain all request functions for Website.
"""

<<<<<<< HEAD
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
    api_name = '/check_login'
    
    response = __request(api_name, item)
    return response

def add_employee(item: dict):
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
    api_name = '/get_history'
    
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
        'code': 'error code!'   ,
    }
    """
    api_name = '/change_password'
    
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
    api_name = '/get_statistics'
    
    response = __request(api_name, item)
    return response
    
def get_all_solutions(item: dict):
    """
    Make a request to database server to get all solutions.

    Returns:
        response = dict(key: value)
    Example:
    >>> get_atll_solutions()
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
    api_name = '/get_all_solutions'
    
    response = __request(api_name, item)
    return response

def get_management_info(item: dict):
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
    
    response = __request(api_name, item)
    return response

def add_garden(item: dict):
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
    
    response = __request(api_name, item)
    return response

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
    response = __request(api_name, item)
    return response

def get_employee_info(item:dict):
    """
    Make a request to database server to get employer infomation.

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
    >>> get_employee_info(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'employee_info' :{
            'ID: [int],
            'Tên nhân viên': [str] 
        }
    }
    """
    api_name = '/get_employee_info'
    response = __request(api_name, item)
    return response

def delete_garden(item:dict):
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
    response = __request(api_name, item)
    return response

def delete_employee(item:dict):
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
    response = __request(api_name, item)
    return response

def task_employee(item = dict):
    """
    Make a request to database server to give task for employee.

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
    >>> task_employee(item=item)
    {
        'message' : 'message!',
        'code': 'error code!',
        'table':{
        "Tên nhân viên: [str]
        "Hàng:[str]}
        }
    }
    """
    api_name = '/task_employee'
    response = __request(api_name, item)
    return response

=======
>>>>>>> packages
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