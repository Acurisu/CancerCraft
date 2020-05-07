# -*- coding: utf-8 -*-

# Generic/Built-in
from importlib import util
from datetime import datetime

def import_file(module_name: str, path: str):
    """
    Imports a module from a file

    Parameters
    ----------
    module_name : str
        name of the module to be imported
    path : str
        absolute path to the module
    """
    spec = util.spec_from_file_location(module_name, path)
    module = util.module_from_spec(spec)

    spec.loader.exec_module(module)
    return module

def get_time():
    """
    Returns the current time as string with format 'Y-m-d H:M:S'
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_uuid(uuid: str):
    """
    Returns UUID formatted according to https://tools.ietf.org/html/rfc4122#section-3 (8-4-4-4-12)

    Parameters
    ----------
    module_name : str
        unformatted UUID
    """
    return f'{uuid[0:8]:s}-{uuid[8:12]:s}-{uuid[12:16]:s}-{uuid[16:20]:s}-{uuid[20:32]:s}'