from src.gui import icons, utils
import os

from PySide2.QtWidgets import QDialog, QMainWindow, QApplication, QPushButton, QVBoxLayout, QListWidget, \
    QListWidgetItem, \
    QFrame, QWidget, \
    QHBoxLayout, QLabel

from PySide2.QtGui import QIcon

from PySide2 import QtCore, QtSvg
from PySide2.QtGui import QCursor

style_ = """
 
    QWidget#layout {
        background: white;
    }
    QLabel#src_file{
        border: 1px solid rgba(0, 0, 0, 0.12);
        background: #efefef;
        color: black;
        font-weight: 200;
        font-size: 14px;
        font-style: normal;
        padding:0px;
        alignment: center;
    }
    
    QLabel#dest_file{
        border: 1px solid rgba(0, 0, 0, 0.12);
        background: #efefef;
        color: black;
        padding:0px;
    }


"""

from PySide2 import QtCore, QtGui, QtWidgets


class JobWidget(QWidget, object):

    set_done_appearence_signal = QtCore.Signal()

    def __init__(self, id, src_file, dest_file, done=False):
        super(JobWidget, self).__init__()
        self.id = id
        self.done = done

        self.src_file = src_file
        self.dest_file = dest_file
        self.widget_layout = QHBoxLayout()
        self.widget_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.widget_layout.addWidget(QLabel(self.src_file))

        arrow = QLabel()
        arrow.setPixmap(icons.load_icon('arrow.svg').pixmap(32))
        self.widget_layout.addWidget(arrow)

        self.widget_layout.addWidget(QLabel(self.dest_file))

        self.setLayout(self.widget_layout)
        self.set_done_appearence_signal.connect(self.set_done_appearence)

        self.show()

    def open(self, *args, **kwargs):
        utils.open_file_exporer(self.dest_file)
        self.hide()
        self.destroy()

    def set_done(self, done):
        if self.done:
            return
        self.done = done
        self.set_done_appearence_signal.emit()

    def set_done_appearence(self):
        check = QLabel()
        check.setPixmap(icons.load_icon('checkmark.svg').pixmap(32))
        button = create_button("Open", event=self.open)

        self.widget_layout.addWidget(check)
        self.widget_layout.addWidget(button)


def create_button(*args, **kwargs):
    e = kwargs.pop("event", None)
    b = QPushButton(*args, **kwargs)
    b.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    if e:
        b.mousePressEvent = e
    return b


def create_button_layout(buttons):
    layout = QVBoxLayout()
    for b in buttons:
        layout.addWidget(b)
    return layout
