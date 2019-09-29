from src.gui import icons

from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon

from PyQt5 import QtCore
from PyQt5.QtGui import QCursor


class ExtendedQListWidgetItem(QListWidgetItem):

    def __init__(self, id, *args, done=False, icon: QIcon=None):
        super(ExtendedQListWidgetItem, self).__init__(*args)
        self.id = id
        self.done = done
        if icon:
            self.setIcon(icon)
            self.setToolTip('Conversion is in progress...')
        self.original_text = args[0] if len(args) else ''

    def set_done(self, done):
        self.done = done
        self.setText(self.original_text + ' - Done')
        self.setIcon(icons.load_icon(icons.IconNames.CHECK_MARK))
        self.setToolTip('Conversion is done, click to remove.')


def create_button(*args, **kwargs):
    class Button(QPushButton):
        pass

    b = QPushButton(*args, **kwargs)
    b.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    return b


def create_button_layout(buttons):
    layout = QVBoxLayout()
    for b in buttons:
        layout.addWidget(b)
    return layout

