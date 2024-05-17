import pickle
from pathlib import Path
import os

def save(obj: object, save_path: str= 'splitted_obj', split_by: int= 5):
    """
    This func will split any obj into smaller part and save it.

    Args:
        obj: object
        save_path: str = 'splitted_obj' (path to save)
        split_by: int = 5 (how many parts)

    Returns:
        None
        
    Example:

    >>> obj = 'this is object'
    >>> save(obj)
    """
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)

    obj_in_bytes = pickle.dumps(obj)

    obj_part_name = 'obj_part_{}.split'

    for i in range(split_by):
        part = int(len(obj_in_bytes)/split_by)
        start = i*part
        end = (i+1)*part

        if i == (split_by - 1):
            splitted_obj = obj_in_bytes[start:]
        else:
            splitted_obj = obj_in_bytes[start: end]

        path = save_path / obj_part_name.format(i+1)

        with open(path, 'wb') as f:
            f.write(splitted_obj)
    
def load(save_path: str = 'splitted_obj'):
    """
    This func will merge the splitted objs in particular path.

    Args:
        save_path: str = 'splitted_obj' (path to merge)

    Returns:
        objects
        
    Example:

    >>> obj = load()
    >>> print(obj)
    'this is object'
    """
    save_path = Path(save_path)
    splitted_obj_paths = os.listdir(save_path)

    obj_in_bytes = b''

    for splitted_obj_path in splitted_obj_paths:
        with open(save_path / splitted_obj_path, 'rb') as f:
            obj_in_bytes += f.read()

    try:
        obj = pickle.loads(obj_in_bytes)
        return obj
    except:
        print('Some files is missing!')

if __name__ == '__main__':
    obj = 'chao em'

    # save(obj)
    obj = load()
    print(obj)