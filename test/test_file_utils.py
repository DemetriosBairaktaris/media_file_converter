
import pytest
from test.files import file_utils

def test_bare_extension():
    ext = '.ext'
    ext1 = 'ext'
    assert file_utils.get_bare_extension(ext) == file_utils.get_bare_extension(ext1) == 'ext'
