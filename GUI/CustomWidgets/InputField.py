from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit


class InputField(QWidget):

    def __init__(self, parent, title, value="", spacing=3, arrangement=None, max_width=None):
        super().__init__(parent)
        if arrangement is None:
            arrangement = [1, 3]
        if max_width:
            self.setMaximumWidth(max_width)
        self.title = title
        self.value = value

        self.title_label = QLabel()
        self.title_label.setText("{}:".format(self.title))

        self.line_edit = QLineEdit()
        self.line_edit.setText(self.value)
        self.line_edit.textChanged.connect(self.handle_text_changed)

        layout = QHBoxLayout()

        layout.addWidget(self.title_label, arrangement[0])
        layout.addWidget(self.line_edit, arrangement[1])

        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(spacing)

        self.setLayout(layout)

    def handle_text_changed(self):
        self.value = self.line_edit.text()
