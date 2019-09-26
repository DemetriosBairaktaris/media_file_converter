from PyQt5.QtWidgets import QApplication
from src.gui.form_window import Dialog, ExtendedQApp
from src.backend.backend import Conversion
import sys


def start_dialog(app, conversion):
    return Dialog(conversion, app=app)


def start_app():
    app = ExtendedQApp([]) #QApplication([])
    app.setQuitOnLastWindowClosed(True)
    dialog = start_dialog(app, Conversion())
    return app, dialog


def main():
    app, dialog = start_app()
    app.exec(dialog)
    app.quitOnLastWindowClosed()


if __name__ == '__main__':
    main()
