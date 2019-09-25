from PyQt5.QtWidgets import QApplication
from src.gui.form_window import Dialog
from src.backend.backend import Conversion
import sys


def start_dialog(app, conversion):
    return Dialog(conversion, app=app)


def start_app():
    app = QApplication([])
    dialog = start_dialog(app, Conversion())
    dialog.show()
    return app


def main():
    app = start_app()
    app.quitOnLastWindowClosed()
    app.exec()


if __name__ == '__main__':
    main()
