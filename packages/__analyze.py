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
    
    response = _request(api_name, item)
    return response