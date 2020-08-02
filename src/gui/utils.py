import os
import subprocess
import sys

from PySide2.QtWidgets import QMessageBox


def open_file_exporer(path):
    path = os.path.normpath(path)

    if sys.platform == 'darwin':
        cmd = 'open -R'
    elif sys.platform == 'win32':
        cmd = 'explorer.exe'
    else:
        # TODO
        pass
    os.system('{} \"{}\"'.format(cmd, path))


def prompt_message_box(app,
                       info,
                       options=(QMessageBox.Yes, QMessageBox.No),
                       default_option=QMessageBox.No):
    if options:
        option = options[0]
        for o in options[1:]:
            option = option | o
    else:
        option = default_option

    box = QMessageBox.question(app, 'Error', info,
                               option, default_option)
    return box
