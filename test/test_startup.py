import pytest
from src.gui import main


def test_startup():
    """Test that the app can simply start"""

    app = main.start_app()
    assert app.thread().isRunning()
    from time import sleep
    sleep(1)
    app.closeAllWindows()

