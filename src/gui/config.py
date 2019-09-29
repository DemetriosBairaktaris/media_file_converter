from src import gui
import os
import json


def load_gui_config():
    path = os.path.dirname(os.path.abspath(gui.__file__))
    path = os.path.join(path, 'config.json')
    return json.load(open(path))



