import os
from test import files


def get_bare_extension(ext):
    ext = ext.split('.')[-1]
    return ext


def get_file_by_type(ext) -> str:
    name = 'file.' + get_bare_extension(ext)
    if os.path.exists(os.path.join(get_files_dir(), name)):
        return os.path.join(get_files_dir(), name)


def get_files_dir():
    path = os.path.dirname(os.path.abspath(files.__file__))
    return path
