import pytest
from src.gui import main
from threading import Thread
from time import sleep

app = None


def kill():
    global app
    while app is None:
        pass
    assert app.thread().isRunning()
    app.closeAllWindows()


def start_app():
    global app
    app, dialog = main.start_app()
    app.exec(dialog)
    pass

@pytest.mark.skip()
def test_startup():
    global app
    """Test that the app can simply start"""
    Thread(target=kill).start()
    start_app()
