from .__request import _request

from .__garden_func.__add_delete import add_garden, delete_garden

from .__query_info.__get_all_solutions import get_all_solutions
from .__query_info.__get_employee_info import get_employee_info
from .__query_info.__get_employee_table import get_location_assignment_table
from .__query_info.__get_gardens_info import get_gardens_info
from .__query_info.__get_management_info import get_management_info
from .__query_info.__get_history import get_history
from .__query_info.__get_statistics import get_statistics

from .__user_func.__add_delete import add_employee, delete_employee
from .__user_func.__assign_employee_location import assign_employee_location
from .__user_func.__change_password import change_password
from .__user_func.__check_login import check_login

from .__analyze import analyze
"""
    Contain all request functions for Website.
"""

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