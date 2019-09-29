from src.gui.config import load_gui_config


def get_style_sheet():
    return """
            QListWidget::item {{ 
                  background-color:#efefef;
                  margin: 5px;
                  margin-bottom:0px; 
                  padding: 3px;
            }}
            QListWidget::item:pressed {{background-color: #000000;}}
            QGroupBox {{background-color: {main_color}; color: {accent_color}}}
            QLabel {{color: {accent_color}}}
            QPushButton {{ background-color: {accent_color}; border: none; color: {main_color}; padding: 5px; border-radius: 3px }}
            QPushButton:hover {{ background-color: #555555}}
                
         
            """.format(**load_gui_config())
