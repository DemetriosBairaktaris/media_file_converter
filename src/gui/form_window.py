import sys
import os
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QFileDialog, QMessageBox, QListWidget, QStyleFactory, QStyle, QListWidgetItem, QSystemTrayIcon)

from src.backend.backend import Jobs
from src.gui.widgets import ExtendedQListWidgetItem


def open_file_exporer(path):
    if sys.platform == 'darwin':
        cmd = 'open'
    else:
        cmd = 'explorer.exe'

    os.system('{} {}'.format(cmd, path))


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


class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, conversion, test_mode=False, app=None, icon=None):
        super(Dialog, self).__init__()
        if app:
            self.app = app
            #self.app.aboutToQuit.connect(self.closeEvent)

        if icon:
            self.sti = QSystemTrayIcon()
            self.sti.setIcon(icon)
            self.menu = QMenu()
            self.sti.show()

        self.start_func = self.handle_start
        self.conversion = conversion
        self.source_button = QPushButton('Select Source')
        self.source_button.clicked.connect(self.openFileNameDialog)

        self.status_list = QListWidget()
        self.status_list.itemClicked.connect(self.item_clicked)
        self.status_list.setStyleSheet(
        '''QListWidget::item { 
                  background-color:#efefef;
                  margin: 5px;
                  margin-bottom:0px; 
                  padding: 3px;
                  
              },
              QListWidget::item:pressed {
                background-color: #000000;
        }''')

        self.jobs = Jobs()
        self.jobs.observers.append(self)
        self.selected_source = QLabel('')
        self.dest_type_picker = QComboBox()

        if test_mode:
            for i in range(10):
                self.status_list.addItem(ExtendedQListWidgetItem(123, 'Text'))
        if not test_mode and conversion is None:
            raise Exception('Conversion backend not found')

        if conversion:
            for t in conversion.get_supported_types():
                self.dest_type_picker.addItem(t)

        self.createFormGroupBox()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.start_func or (lambda *args: 0))
        buttonBox.rejected.connect(self.close)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("FILE CONVERTER")

    def notify(self, job, *args, **kwargs):
        id = job.id
        index = self.jobs.index_of_id(id)
        text = self.status_list.item(index).text()

        self.status_list.item(index).setText(text + ' - Done')

    def handle_start(self, *args, **kwargs):
        selected_conversion_type = self.dest_type_picker.currentText()
        selected_source = self.get_selected_source()

        thread = None
        params = (selected_source, selected_conversion_type)
        kwparams = {'app_window': self}
        convert = self.conversion.convert
        try:
            thread = convert(*params, **kwparams)
        except FileExistsError:
            if prompt_message_box(self, 'File already exists...do you want to overwrite?') == QMessageBox.Yes:
                try:
                    kwparams['check_file_path'] = False
                    thread = convert(*params, **kwparams)
                except FileExistsError:
                    prompt_message_box(self, 'Destination and Source are the same...no need to convert',
                                       options=[], default_option=QMessageBox.Ok)
                    thread = None

        if thread is not None:
            text = 'Currently converting ' + self.get_selected_source()
            src_path_without_ext, ext = os.path.splitext(self.get_selected_source())
            dest_path = os.path.join(src_path_without_ext + '.' + selected_conversion_type)
            self.jobs.add_job(thread, text, self.get_selected_source(), dest_path)
            item = ExtendedQListWidgetItem(self.jobs[-1].id, text)
            self.status_list.addItem(item)

    def set_selected_source(self, path):
        if path:
            self.selected_source.setText(path)
            print(str(self.get_selected_source()))

    def get_selected_source(self):
        return self.selected_source.text()

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Convert File")
        layout = QFormLayout()
        layout.addRow(QLabel("Source Path"), self.source_button)
        layout.addRow(self.selected_source)
        layout.addRow(QLabel("Convert to type:"), self.dest_type_picker)
        layout.addRow(self.status_list)
        self.formGroupBox.setLayout(layout)

    def item_clicked(self, item, *args):
        if self.jobs.get_job(item.id).is_done():
            open_file_exporer(self.jobs[self.jobs.index_of_id(item.id)].get_dest_path())
            self.status_list.takeItem(self.jobs.index_of_id(item.id))
            self.jobs.remove_job_by_id(item.id)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        self.set_selected_source(fileName)

    def closeEvent(self, QCloseEvent):

        self.jobs.stop_polling_for_jobs(wait=True)


class ExtendedQApp(QApplication):

    def exec(self, dialog):
        dialog.exec()
        pass


if __name__ == '__main__':
    app = ExtendedQApp(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    dialog = Dialog(None, app=app, test_mode=True)
    app.exec(dialog)
    app.instance().quit()
    pass
