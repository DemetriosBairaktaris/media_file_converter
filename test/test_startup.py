import pytest
from src.gui import main
from threading import Thread
from time import sleep

app = None
running = None


def kill():
    global app
    global running
    while app is None:
        sleep(1)
    running = app.thread().isRunning()
    app.quit()


def start_app():
    global app
    app, dialog = main.start_app()
    app.exec(dialog)
    pass


#@pytest.mark.skip()
def test_startup():
    global app
    global running
    """Test that the app can simply start"""
    t = Thread(target=kill)
    t.start()
    start_app()
    t.join()
    assert running is True
