import pytest
import sys
from src.gui import main


def test_startup():
    app = main.start_app()
    assert app.thread().isRunning()
    app.instance().exit(0)
