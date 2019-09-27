import os
from src import gui

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class IconNames:
    CHECK_MARK = 'checkmark.svg'


def load_icon(icon_name):
    _, ext = (os.path.splitext(icon_name))
    full_path = os.path.join(get_icon_dir_path(ext[1:]), icon_name)
    if os.path.exists(full_path):
        return QIcon(full_path)
    raise FileNotFoundError


def get_icon_dir_path(suffix):
    path = os.path.dirname(os.path.abspath(gui.__file__))
    path = os.path.join(path, 'icons_' + suffix)

    return path
