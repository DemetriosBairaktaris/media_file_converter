from src.gui import icons

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon


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
