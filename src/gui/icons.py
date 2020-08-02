import os
import sys
from src import gui

from PySide2.QtGui import QIcon, QMovie
from PySide2.QtCore import QByteArray, QBuffer


class IconNames:
    CHECK_MARK = 'checkmark.svg'
    SPINNER = 'spinner.gif'


def load_icon(icon_name):
    _, ext = (os.path.splitext(icon_name))
    full_path = os.path.join(get_icon_dir_path(ext[1:]), icon_name)
    if os.path.exists(full_path):
        return QIcon(full_path)
    raise FileNotFoundError


def load_gif(gif_name):
    _, ext = (os.path.splitext(gif_name))
    full_path = os.path.join(get_icon_dir_path(ext[1:]), gif_name)
    if os.path.exists(full_path):
        gif_byte_array = QByteArray(open(full_path, 'rb').read())
        gif_buffer = QBuffer(gif_byte_array)

        q_movie = QMovie(full_path)
        q_movie.setFormat(QByteArray(b'GIF'))
        q_movie.setDevice(gif_buffer)
        q_movie.setCacheMode(QMovie.CacheAll)
        q_movie.setSpeed(100)
        q_movie.jumpToFrame(0)

        return q_movie
    raise FileNotFoundError


def get_icon_dir_path(suffix):
    path = os.path.dirname(os.path.abspath(gui.__file__))
    if getattr(sys, 'frozen', False):
        path = get_mac_bundle_resources_path()

    path = os.path.join(path, 'icons_' + suffix)

    return path


def get_mac_bundle_resources_path():
    path = os.path.dirname(sys._MEIPASS)
    path = os.path.join(path, 'Resources')
    return path