from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QFileDialog, QMessageBox, QListWidget, QStyleFactory, QStyle, QListWidgetItem)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class ExtendedQListWidgetItem(QListWidgetItem):

    def __init__(self, id, *args):
        self.id = id
        super(ExtendedQListWidgetItem, self).__init__(*args)