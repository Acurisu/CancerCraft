# -*- coding: utf-8 -*-

# Generic/Built-in
from importlib import util
from datetime import datetime

def import_file(module_name, path):
    spec = util.spec_from_file_location(module_name, path)
    module = util.module_from_spec(spec)

    spec.loader.exec_module(module)
    return module

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_uuid(uuid):
    return f'{uuid[0:8]:s}-{uuid[8:12]:s}-{uuid[12:16]:s}-{uuid[16:20]:s}-{uuid[20:32]:s}'