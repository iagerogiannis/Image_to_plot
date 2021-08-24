from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QGroupBox, QVBoxLayout, QRadioButton


class AxisSystemDefinitionPopUp(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Axis System Definition")
        self.resize(250, 200)
        self.ortho = True
        self.points = 0

        self.ortho_buttons_count = 0
        self.point_buttons_count = 0

        self.ortho_layout = QGridLayout()
        self.points_layout = QGridLayout()

        self.point_buttons = []

        self.addPointsRadioButton(True)
        self.addPointsRadioButton()
        self.addPointsRadioButton()
        self.addPointsRadioButton(enabled=False)

        self.addOrthoRadioButton("Ortho", True, True)
        self.addOrthoRadioButton("Lateral", False)

        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.pressed.connect(self.proceed_button_pressed)

        ortho_group = QGroupBox(self)
        ortho_group.setTitle("Ortho/ Lateral")
        ortho_group.setLayout(self.ortho_layout)

        points_group = QGroupBox(self)
        points_group.setTitle("Number of Points/ Levels")
        points_group.setLayout(self.points_layout)

        central_layout = QVBoxLayout()
        central_layout.addWidget(ortho_group)
        central_layout.addWidget(points_group)
        central_layout.addWidget(self.proceed_button)
        self.setLayout(central_layout)

    def addRadioButton(self, name, on_click=lambda: None, layout=None, layout_position=None, checked=False,
                       enabled=True, vertical_alignment=False):
        radiobutton = QRadioButton(name)
        radiobutton.setChecked(checked)
        radiobutton.setEnabled(enabled)
        radiobutton.toggled.connect(on_click)
        if vertical_alignment:
            layout.addWidget(radiobutton, layout_position, 0)
        else:
            layout.addWidget(radiobutton, 0, layout_position)
        return radiobutton

    def addOrthoRadioButton(self, name, ortho=False, checked=False, enabled=True):
        radiobutton = self.addRadioButton(name, self.ortho_clicked, self.ortho_layout, self.ortho_buttons_count, checked,
                                          enabled)
        radiobutton.ortho = ortho
        self.ortho_buttons_count += 1
        return radiobutton

    def addPointsRadioButton(self, checked=False, enabled=True):
        radiobutton = self.addRadioButton(self.point_button_name(self.point_buttons_count), self.points_clicked, self.points_layout, self.point_buttons_count, checked,
                                          enabled, True)
        radiobutton.points = self.point_buttons_count
        self.point_buttons_count += 1
        self.point_buttons.append(radiobutton)

    def point_button_name(self, points):
        if self.ortho:
            return "{} Points / {} Levels".format(str(points), str(4 - 2 * points))
        else:
            return "{} Points / {} Levels".format(str(points), str(6 - 2 * points))

    def ortho_clicked(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.ortho = radio_button.ortho
            self.point_buttons[3].setEnabled(not self.ortho)
            if self.point_buttons[3].isChecked() and not self.point_buttons[3].isEnabled():
                self.point_buttons[2].setChecked(True)
            for i in range(len(self.point_buttons)):
                self.point_buttons[i].setText(self.point_button_name(i))

    def points_clicked(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.points = radio_button.points

    def proceed_button_pressed(self):
        if self.ortho:
            self.levels = 4 - 2 * self.points
        else:
            self.levels = 6 - 2 * self.points
        self.accept()

    def resizeEvent(self, a0):
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
