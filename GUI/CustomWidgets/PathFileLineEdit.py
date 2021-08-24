from PyQt5.QtWidgets import QLineEdit, QFileDialog


class PathFileLineEdit(QLineEdit):

    def __init__(self, parent, placeholder, default_path="C:\\", filename="", filters=""):
        super().__init__(parent)
        self.parent = parent
        self.setPlaceholderText(placeholder)
        self.default_path = default_path
        self.filename = filename
        self.filters = filters

    def mouseDoubleClickEvent(self, event):
        file_path = QFileDialog.getSaveFileName(None, caption='Export file:',
                                                directory=r"{}/{}".format(self.default_path, self.filename),
                                                filter=self.filters)[0]

        if file_path != "":
            self.setText(file_path)
