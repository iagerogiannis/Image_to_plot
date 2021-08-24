from PyQt5.QtWidgets import QMainWindow, QDialog
from GUI.Components.Workspace import Workspace
from GUI.MainMenu import MainMenu
from GUI.PopUps.ExportPopUp import ExportPopUp
from GUI.PopUps.AxisSystemCalibrationPopUp import AxisSystemCalibrationPopUp
from GUI.PopUps.AxisSystemDefinitionPopUp import AxisSystemDefinitionPopUp


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(200, 80, 1000, 600)
        self.setWindowTitle("Image to Plot with Splines")

        self.mainMenu = MainMenu(self)
        self.workspace = Workspace(self)
        self.setCentralWidget(self.workspace)
        self.show()

    def call_axis_system_definition_pop_up(self):
        definition_pop_up = AxisSystemDefinitionPopUp(self)
        if definition_pop_up.exec_() == QDialog.Accepted:
            return {"ortho": definition_pop_up.ortho,
                    "points": definition_pop_up.points,
                    "levels": definition_pop_up.levels}

    def call_calibration_pop_up(self, points, levels):
        calibration_pop_up = AxisSystemCalibrationPopUp(self, points, levels)
        if calibration_pop_up.exec_() == QDialog.Accepted:
            return calibration_pop_up.values

    def call_export_pop_up(self):
        export_pop_up = ExportPopUp(self)
        if export_pop_up.exec_() == QDialog.Accepted:
            return {"axis_system_id": export_pop_up.selected_axis_system_id,
                    "graph_names": export_pop_up.selected_shape_names,
                    "graph_ids": export_pop_up.selected_shape_ids,
                    "filepath": export_pop_up.filepath,
                    "dx_division": export_pop_up.dx_division,
                    "num_of_divisions": export_pop_up.num_of_divisions_value}
        else:
            return None
