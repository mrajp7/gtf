from datetime import datetime
import jmespath
import os
import os.path
from gtf.common.logger import Logger as logger

TAG = 'Utils'

def create_time_stamped_dir(path='', prefix=''):
    '''
    Creates a dir with a time stamp in given path
    
    Args:
        path (str): parent dir path to create dir
        prefix (str): A prefix to add before the timestamp in the dir name
    '''
    logger.log_info(TAG, 'Creating time-stamped directory')
    dir_path = os.path.join(path, prefix + datetime.now().strftime('_%Y-%m-%d_%X'))
    os.makedirs(dir_path)
    logger.log_info(TAG, 'Created' + dir_path)
    return dir_path


def resolve_jmes(path, json_obj):
    '''
    Returns the value of the JMES Path in the given JSON
    
    Args:
        path (str): JMES Path
        json_obj (dict): JSON Obj
    '''
    return jmespath.search(path, json_obj)
