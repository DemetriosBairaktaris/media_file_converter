from src.gui.form_window import Dialog, ExtendedQApp, SystemTrayIcon
from src.backend.backend import Conversion


def start_dialog(conversion):
    return Dialog(conversion)


def start_app():
    app = ExtendedQApp()
    app.setQuitOnLastWindowClosed(True)
    dialog = start_dialog(Conversion())
    return app, dialog


def main():
    app, dialog = start_app()
    system_tray = SystemTrayIcon(dialog)
    system_tray.show()
    app.exec_()


if __name__ == '__main__':
    main()
