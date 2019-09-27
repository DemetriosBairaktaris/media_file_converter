import pytest
from src.gui import icons
from src.gui.icons import IconNames


def test_load_icon():
    assert icons.load_icon(IconNames.CHECK_MARK)


def test_load_icon_non_existent():
    with pytest.raises(FileNotFoundError):
        icons.load_icon('notareal.svg')
