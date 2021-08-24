from PyQt5.QtWidgets import QMessageBox, QGridLayout, QGroupBox, QVBoxLayout, QDialog, QPushButton
from GUI.CustomWidgets.InputField import InputField


class AxisSystemCalibrationPopUp(QDialog):

    def __init__(self, parent, points, levels):
        super().__init__(parent)
        levels = levels // 2
        self.values = {"points": [[], []],
                       "levels": [[], []]}

        self.point_inputs = [[], []]
        self.level_inputs = [[], []]

        complete_button = QPushButton("Complete Calibration")
        complete_button.clicked.connect(self.handle_complete_calibration)

        grid = QGridLayout()
        if points:
            grid.addWidget(self.create_point_group(points), 0, 0, 1, 2)
        if levels:
            grid.addWidget(self.create_level_group("X", levels), 1, 0)
            grid.addWidget(self.create_level_group("Y", levels), 1, 1)
        grid.addWidget(complete_button, 2, 0, 1, 2)
        self.setLayout(grid)

        self.setWindowTitle("Axis System Calibration")
        self.setFixedWidth(250)

    def create_point_group(self, num_of_fields):
        group_box = QGroupBox("Points")
        grid = QGridLayout()
        for i in range(num_of_fields):
            for j, coord in enumerate(["X", "Y"]):
                self.point_inputs[j].append(InputField(self, "P{} {}".format(str(i), coord)))
                grid.addWidget(self.point_inputs[j][-1], i, j)
        group_box.setLayout(grid)
        return group_box

    def create_level_group(self, label, num_of_fields):
        if label == "X":
            j = 0
        else:
            j = 1
        group_box = QGroupBox("{} Levels".format(label))
        vbox = QVBoxLayout()
        for i in range(num_of_fields):
            self.level_inputs[j].append(InputField(self, "L{}{}".format(label, str(i))))
            vbox.addWidget(self.level_inputs[j][-1])
        group_box.setLayout(vbox)
        return group_box

    def set_values(self):
        for i in range(2):
            for j in range(len(self.point_inputs[0])):
                self.values["points"][i].append(float(self.point_inputs[i][j].value))
            for j in range(len(self.level_inputs[0])):
                self.values["levels"][i].append(float(self.level_inputs[i][j].value))

    def reset_values(self):
        self.values = {"points": [[], []],
                       "levels": [[], []]}

    def handle_complete_calibration(self):
        try:
            self.set_values()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Error", "Wrong Input!")
            self.reset_values()

    def resizeEvent(self, a0):
        self.setFixedHeight(self.height())
