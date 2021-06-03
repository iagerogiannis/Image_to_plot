import os

from PyQt5.QtWidgets import QPushButton


class ToolbarButton(QPushButton):

    def __init__(self, parent, text, triggered_function=None, image_fname=None, tooltip="", checkable=False):
        super().__init__()
        self.parent = parent
        self.text = text
        self.setFixedSize(32, 32)
        self.triggered_function = triggered_function
        self.setFlat(True)
        self.setCheckable(checkable)
        if self.triggered_function:
            self.clicked.connect(self.triggered_function)
        if image_fname:
            self.image_fname = image_fname
            image_default_path = r"{}\icons\default\{}".format(os.getcwd(), self.image_fname).replace("\\", "/")
            image_hover_path = r"{}\icons\hover\{}".format(os.getcwd(), self.image_fname).replace("\\", "/")
            self.setStyleSheet("""
            QPushButton {{
                background-image: url("{}");
                background-repeat: no-repeat;
                background-position: center;
            }} 
            QPushButton::hover {{
                background-image: url("{}");
                background-repeat: no-repeat;
                background-position: center;
            }} 
            QPushButton::checked {{
                background-image: url("{}");
                background-repeat: no-repeat;
                background-position: center;
            }} 
            """.format(image_default_path, image_hover_path, image_hover_path))
        else:
            self.setText(text)
        if tooltip != "":
            self.setToolTip(tooltip)
