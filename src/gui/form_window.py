import os

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtWidgets import (QApplication, QComboBox, QDialog, QScrollArea,
                               QFormLayout, QGroupBox, QDesktopWidget, QLabel,
                               QVBoxLayout, QFileDialog, QMessageBox, QListWidget, QListWidgetItem)

from src.backend.backend import Jobs
from src.gui import icons, style, utils
from src.gui import widgets


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        self.icon = icons.load_icon('icon.svg')
        QtWidgets.QSystemTrayIcon.__init__(self, self.icon, parent)
        self.parent: QDialog = parent
        self.activated.connect(self.on_click)

    def on_click(self, *args, **kwargs):
        if self.parent.isVisible():
            self.parent.hide()
        else:
            self.parent.show()
            self.parent.topLevelWidget()


class Dialog(QDialog):

    def __init__(self, conversion, test_mode=False):
        super(Dialog, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(style.get_style_sheet())

        self.conversion = conversion
        self.source_button = widgets.create_button('Select Source', event=self.open_file_name_dialog)

        self.status_list = QGroupBox()
        self.status_list_layout = QVBoxLayout()
        self.status_list.setLayout(self.status_list_layout)

        self.jobs = Jobs()
        self.jobs.observers.append(self)
        self.selected_source = QLabel('')
        self.dest_type_picker = QComboBox()
        self.job_widgets: dict = {}

        if test_mode:
            for i in range(400):
                item = widgets.JobWidget(123,
                                               'Text.mp4',
                                               'Text.mp3')
                self.status_list_layout.addWidget(item)

        if not test_mode and conversion is None:
            raise Exception('Conversion backend not found')

        if conversion:
            for t in conversion.get_supported_types():
                self.dest_type_picker.addItem(t)


        self.create_form_group_box()

        self.convert_button = widgets.create_button('Start Converting', event=self.handle_start)
        self.cancel_button = widgets.create_button('Exit', event=self.close_app)
        buttonBox = widgets.create_button_layout([self.convert_button, self.cancel_button])

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addLayout(buttonBox, stretch=False)
        self.setLayout(mainLayout)
        self.setWindowTitle("FILE CONVERTER")

    def notify(self, job, *args, **kwargs) -> bool:
        if job.id not in self.job_widgets:
            return False
        widget: widgets.JobWidget = self.job_widgets[job.id]
        widget.set_done(True)
        del self.job_widgets[job.id]
        return True

    def close_app(self, *args, **kwargs):
        self.close()

    def handle_start(self, *args, **kwargs):
        selected_conversion_type = self.dest_type_picker.currentText()
        selected_source = self.get_selected_source()
        if not selected_source:
            utils.prompt_message_box(self, 'Nothing Selected...', options=[], default_option=QMessageBox.Ok)
            return

        thread = None
        params = (selected_source, selected_conversion_type)
        kwparams = {}
        convert = self.conversion.convert
        try:
            thread = convert(*params, **kwparams)
        except FileExistsError:
            if utils.prompt_message_box(self, 'File already exists...do you want to overwrite?') == QMessageBox.Yes:
                try:
                    kwparams['check_file_path'] = False
                    thread = convert(*params, **kwparams)
                except FileExistsError:
                    utils.prompt_message_box(self, 'Destination and Source are the same...no need to convert',
                                             options=[], default_option=QMessageBox.Ok)
                    thread = None

        if thread is not None:
            text = 'Currently converting ' + self.get_selected_source()
            src_path_without_ext, ext = os.path.splitext(self.get_selected_source())
            dest_path = os.path.join(src_path_without_ext + '.' + selected_conversion_type)
            self.jobs.add_job(thread, text, self.get_selected_source(), dest_path)
            job_id = self.jobs[-1].id
            item = widgets.JobWidget(job_id, text, dest_path)
            self.status_list_layout.addWidget(item)
            self.job_widgets[job_id] = item

    def set_selected_source(self, path):
        if path:
            self.selected_source.setText(path)

    def get_selected_source(self):
        return self.selected_source.text()

    def move_top_left(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def create_form_group_box(self):
        self.formGroupBox = QGroupBox("Convert File")
        layout = QFormLayout()
        layout.addRow(QLabel("Source Path"), self.source_button)
        layout.addRow(self.selected_source)
        layout.addRow(QLabel("Convert to type:"), self.dest_type_picker)
        layout.addRow(self.status_list)
        self.formGroupBox.setLayout(layout)

    def open_file_name_dialog(self, *args, **kwargs):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        self.set_selected_source(fileName)

    def closeEvent(self, QCloseEvent):
        self.jobs.stop_polling_for_jobs(wait=True)


class ExtendedQApp(QApplication):

    def __init__(self):
        super(ExtendedQApp, self).__init__([])
        pass
