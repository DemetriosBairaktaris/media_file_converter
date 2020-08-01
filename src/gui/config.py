import os
import json

from src import gui


def load_gui_config():
    path = os.path.dirname(os.path.abspath(gui.__file__))
    path = os.path.join(path, 'config.json')
    return json.load(open(path))



