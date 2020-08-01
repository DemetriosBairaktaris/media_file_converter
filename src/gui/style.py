from src.gui.config import load_gui_config


def color_with_opacity(hex_value, opacity):
    hex_value = hex_value.replace('#', "")
    r, g, b = (int(x, 16) for x in [hex_value[:2], hex_value[2:4], hex_value[4:6]])
    return "rgba({},{},{},{})".format(r, g, b, opacity)


def get_style_sheet():
    config = load_gui_config
    accent_color = config()['accent_color']
    style_sheet = """    
    QListWidget::item {{ 
          background-color:#efefef;
          margin: 5px;
          margin-bottom:0px; 
          padding: 3px;
    }}
    QListWidget::item:pressed {{background-color: #000000;}}
    QGroupBox {{background-color: {main_color}; color: {accent_color}}}
    QLabel {{color: {accent_color}}}
    QPushButton {{ background-color: {accent_color}; border: none; color: {main_color}; padding: 5px; border-radius: 3px}}
    QPushButton:hover {{background: {color_with_opacity}}}
    QDialog{{background-color: {main_color}}}"""

    return style_sheet.format(**config(), color_with_opacity=color_with_opacity(accent_color, .9))
