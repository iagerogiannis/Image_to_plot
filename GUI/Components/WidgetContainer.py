from PyQt5.QtWidgets import QFrame, QVBoxLayout


class WidgetContainer(QFrame):

    def __init__(self, parent, widget):
        super().__init__(parent)
        self.canvas = widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


class CanvasContainer(WidgetContainer):

    def __init__(self, parent, widget):
        super().__init__(parent, widget)
        self.setStyleSheet("""margin: 0px;
                              border: 1px solid rgb(130, 135, 144);
                              padding: 0px;""")
