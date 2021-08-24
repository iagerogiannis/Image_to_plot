from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QComboBox, QGroupBox, QCheckBox, QGridLayout, QMessageBox, QRadioButton
from GUI.CustomWidgets.PathFileLineEdit import PathFileLineEdit
from GUI.CustomWidgets.InputField import InputField


class ExportPopUp(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.selected_shape_ids = []
        self.selected_shape_names = []
        self.selected_axis_system_id = None
        self.dx_division = True
        self.filepath = ""

        self.setWindowTitle("Export Data")

        self.axis_group = QGroupBox(self)
        self.axis_group.setTitle("Axis System")

        axis_systems = [axis_system["Name"] for axis_system in self.parent.workspace.shapes_tree.get_axis_systems()]
        self.axis_system_ids = [axis_system["id"] for axis_system in self.parent.workspace.shapes_tree.get_axis_systems()]

        self.axis_systems = QComboBox(self.axis_group)
        self.axis_systems.addItem("(Choose Axis System)")
        for axis_system in axis_systems:
            self.axis_systems.addItem(axis_system)

        self.axis_layout = QVBoxLayout(self.axis_group)
        self.axis_layout.addWidget(self.axis_systems)
        self.axis_group.setLayout(self.axis_layout)

        self.shapes_group = QGroupBox(self)
        self.shapes_group.setTitle("Shapes")

        shapes = [shape["Name"] for shape in self.parent.workspace.shapes_tree.get_shapes()]

        self.shape_ids = [shape["id"] for shape in self.parent.workspace.shapes_tree.get_shapes()]

        self.shapes = []
        for shape in shapes:
            self.add_shape(shape)

        self.shapes_layout = QGridLayout(self.shapes_group)
        self.arrange_shapes_layout()
        self.shapes_group.setLayout(self.shapes_layout)

        self.options_group = QGroupBox(self)
        self.options_group.setTitle("Spline Options")

        self.radio_buttons = [QRadioButton(self.options_group) for i in range(2)]
        self.radio_buttons[0].dx_division = True
        self.radio_buttons[0].setText("dx Division")
        self.radio_buttons[0].setChecked(True)
        self.radio_buttons[1].dx_division = False
        self.radio_buttons[1].setText("dt Division")
        for radio in self.radio_buttons:
            radio.toggled.connect(self.handle_radio_toggled)

        self.num_of_divisions_value = 200
        self.num_of_divisions = InputField(self.options_group, "Number of Points", str(self.num_of_divisions_value),
                                           10, [2, 1], 170)

        self.options_layout = QGridLayout(self.options_group)
        for i in range(2):
            self.options_layout.addWidget(self.radio_buttons[i], 0, i)
        self.options_layout.addWidget(self.num_of_divisions, 1, 0, 1, 2)

        self.options_group.setLayout(self.options_layout)

        self.export_group = QGroupBox(self)
        self.export_group.setTitle("File Export")

        self.filepath_line_edit = PathFileLineEdit(self.export_group, "Export File", filename="plot_data",
                                                   filters="Excel Workbook (*.xlsx);; CSV (Comma Delimited) (*.csv)")

        self.export_layout = QVBoxLayout(self.export_group)
        self.export_layout.addWidget(self.filepath_line_edit)
        self.export_group.setLayout(self.export_layout)

        self.export_button = QPushButton(self)
        self.export_button.setText("Export")
        self.export_button.pressed.connect(self.handle_export)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.axis_group)
        self.layout.addWidget(self.shapes_group)
        self.layout.addWidget(self.options_group)
        self.layout.addWidget(self.export_group)
        self.layout.addWidget(self.export_button)
        self.setLayout(self.layout)

        self.setFixedSize(380, 300 + 10 * (len(self.shapes) + len(self.shapes) % 2))
        self.show()

    def handle_radio_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.dx_division = radio_button.dx_division

    def arrange_shapes_layout(self):
        i = 0
        n = len(self.shapes)
        rows = divmod(n + 1, 2)[0]
        for shape in self.shapes:
            col, row = divmod(i, rows)
            self.shapes_layout.addWidget(shape, row, col)
            i += 1

    def add_shape(self, shape_name):
        self.shapes.append(QCheckBox(shape_name))

    def handle_export(self):

        def is_int(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        self.selected_shape_ids = [self.shape_ids[i] for i in range(len(self.shapes)) if self.shapes[i].isChecked()]
        self.selected_shape_names = [shape.text() for shape in self.shapes if shape.isChecked()]
        if self.axis_systems.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Please select an Axis System!")
        elif len(self.selected_shape_ids) == 0:
            QMessageBox.warning(self, "Error", "Please select an least one graph for export!")
        elif self.filepath_line_edit.text() == "":
            QMessageBox.warning(self, "Error", "Please define file path!")
        elif not is_int(self.num_of_divisions.value):
            QMessageBox.warning(self, "Error", "Please define file path!")
        else:
            self.filepath = self.filepath_line_edit.text()
            self.num_of_divisions_value = int(self.num_of_divisions.value)
            self.selected_axis_system_id = self.axis_system_ids[self.axis_systems.currentIndex() - 1]
            self.accept()

    def closeEvent(self, a0):
        self.reject()
