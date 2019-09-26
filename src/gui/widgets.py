from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QFileDialog, QMessageBox, QListWidget, QStyleFactory, QStyle, QListWidgetItem)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class ExtendedQListWidgetItem(QListWidgetItem):

    def __init__(self, id, *args, done=False):
        self.id = id
        self.done = done
        super(ExtendedQListWidgetItem, self).__init__(*args)
        self.original_text = args[0] if len(args) else ''

    def set_done(self, done):
        self.done = done
        self.setText(self.original_text + ' - Done')
