from src.gui import icons, config

from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QWidget
from PyQt5.QtGui import QIcon, QWindow, QColor, QPalette

from PyQt5 import QtCore
from PyQt5.QtGui import QCursor


class ExtendedQListWidgetItem(QListWidgetItem, QWidget):

    def __init__(self, id, *args, done=False, icon: QIcon = None):
        super(ExtendedQListWidgetItem, self).__init__(*args)
        self.id = id
        self.done = done
        if icon:
            self.setIcon(icon)
            self.setToolTip('Conversion is in progress...')
        self.original_text = args[0] if len(args) else ''
        self.setBackground(QColor('#EFEFEF'))

        pass

    def set_done(self, done):
        self.done = done
        color = config.load_gui_config()['success_color']
        self.setBackground(QColor(color))
        self.setText(self.original_text + ' - Done')
        self.setIcon(icons.load_icon(icons.IconNames.CHECK_MARK))
        self.setToolTip('Conversion is done, click to remove.')


def create_convert_item_layout(src_name, dest_name, icon: QIcon, status_icon: QIcon):
    box = QHBoxLayout()
    img = QLabel()
    img.setPixmap(icon.pixmap(50))
    box.addWidget(img)
    box.addWidget(QLabel(src_name))
    box.addWidget(QLabel(dest_name))

    return box


def create_convert_item_widget(src_name, dest_name, icon: QIcon, status_icon: QIcon):
    class ConvertItemWidget(QWidget):
        def __init__(self, src_name, dest_name, icon: QIcon, status_icon: QIcon):
            super(QWidget, self).__init__()

            status_icon = QIcon(icons.load_icon('checkmark.svg'))
            self.setLayout(create_convert_item_layout(src_name, dest_name, icon, status_icon))

            from datetime import datetime
            self.setObjectName('lalal' + str(hash(datetime.now())))

    return ConvertItemWidget(src_name, dest_name, icon, status_icon)


def create_convert_item_collection_layout(*args):
    box = QVBoxLayout()
    for arg in args:
        box.addWidget(arg)
    return box


def create_button(*args, **kwargs):
    b = QPushButton(*args, **kwargs)
    b.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    return b


def create_button_layout(buttons):
    layout = QVBoxLayout()
    for b in buttons:
        layout.addWidget(b)
    return layout
