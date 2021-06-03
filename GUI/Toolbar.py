from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QFrame
from PyQt5.QtCore import Qt

from GUI.ToolbarButton import ToolbarButton


class Toolbar(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.buttons = [ToolbarButton(self, "LI", self.handle_load_image, "import.png", "Import Image"),
                        ToolbarButton(self, "EF", self.handle_load_image, "export.png", "Export Data"),
                        ToolbarButton(self, "AA", self.handle_draw_point, "axis.png", "Set Axis System"),
                        ToolbarButton(self, "DP", self.handle_draw_point, "point.png", "Draw Point"),
                        ToolbarButton(self, "DL", self.handle_draw_line, "line.png", "Draw Line"),
                        ToolbarButton(self, "DPL", self.handle_draw_polyline, "polyline.png", "Draw Polyline"),
                        ToolbarButton(self, "DB", self.handle_draw_bezier, "b_spline.png", "Draw Bezier Spline"),
                        ToolbarButton(self, "DQB", self.handle_draw_quadratic_bezier, "b2_spline.png", "Draw Composite Quadratic Bezier Spline"),
                        ToolbarButton(self, "DCB", self.handle_draw_cubic_bezier, "b3_spline.png", "Draw Composite Cubic Bezier Spline"),
                        ToolbarButton(self, "ED", self.handle_edit, "edit.png", "Edit", checkable=True),
                        ToolbarButton(self, "ER", self.handle_erase, "erase.png", "Erase")
                        ]

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(1, 0, 0, 0)
        self.layout.setSpacing(4)

        for i in range(2):
            self.layout.addWidget(self.buttons[i])

        num_of_sep_lines = 3
        self.separator_lines = [QFrame() for i in range(num_of_sep_lines)]
        for i in range(num_of_sep_lines):
            self.separator_lines[i].setFrameShape(QFrame.HLine)
            self.separator_lines[i].setStyleSheet("color: rgb(211, 211, 211);")

        self.layout.addWidget(self.separator_lines[0])
        self.layout.addWidget(self.buttons[2])
        self.layout.addWidget(self.separator_lines[1])

        for i in range(3, 9):
            self.layout.addWidget(self.buttons[i])

        self.layout.addWidget(self.separator_lines[2])

        for i in range(9, len(self.buttons)):
            self.layout.addWidget(self.buttons[i])

        self.setLayout(self.layout)

    def handle_load_image(self):
        filename = QFileDialog.getOpenFileNames(self, "Select Image", filter="Image Files (*.jpg *.jpeg *.png)")[0]
        if filename:
            self.parent.canvas.load_image(filename[0])
            self.parent.canvas.draw()

    def handle_draw_point(self):
        self.parent.canvas.draw_shape("point")

    def handle_draw_line(self):
        self.parent.canvas.draw_shape("line")

    def handle_draw_polyline(self):
        self.parent.canvas.draw_shape("polyline")

    def handle_draw_bezier(self):
        self.parent.canvas.draw_shape("bezier")

    def handle_draw_quadratic_bezier(self):
        self.parent.canvas.draw_shape("comp_quad_bezier")

    def handle_draw_cubic_bezier(self):
        self.parent.canvas.draw_shape("comp_cub_bezier")

    def handle_edit(self):
        pass

    def handle_erase(self):
        pass
