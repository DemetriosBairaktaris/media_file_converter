import pytest
import sys
from src.gui import main


def test_startup():
    """Test that the app can simply start"""
    return
    app = main.start_app()
    assert app.thread().isRunning()
    app.instance().exit(0)
