from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from GUI.WidgetContainer import *
from GUI.Toolbar import Toolbar
from GUI.CanvasInteractive import CanvasInteractive
from GUI.ShapesTree import ShapesTree


class Workspace(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pan_active = False
        self.zoom_active = False

        self.canvas = CanvasInteractive()
        self.w_canvas = CanvasContainer(self, self.canvas)

        self.canvasToolbar = NavigationToolbar(self.canvas, self)
        self.canvasToolbar.actions()[0].triggered.connect(self.home_callback)
        self.canvasToolbar.actions()[4].triggered.connect(self.pan_callback)
        self.canvasToolbar.actions()[5].triggered.connect(self.zoom_callback)

        self.customToolbar = Toolbar(self)

        self.shapes_tree = ShapesTree(self)
        self.w_shapes_tree = WidgetContainer(self, self.shapes_tree)

        self.workspace_layout = QHBoxLayout()
        self.workspace_layout.addWidget(self.customToolbar, 1)
        self.workspace_layout.addWidget(self.w_canvas, 75)
        self.workspace_layout.addWidget(self.w_shapes_tree, 25)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvasToolbar)
        self.layout.addLayout(self.workspace_layout)
        self.setLayout(self.layout)

    def handle_connection(self):
        if self.pan_active or self.zoom_active:
            self.canvas.pause_interaction()
        else:
            self.canvas.resume_interaction()

    def pan_callback(self):
        if self.pan_active:
            self.pan_active = False
        elif self.zoom_active:
            self.pan_active = True
            self.zoom_active = False
        else:
            self.pan_active = True
        self.handle_connection()

    def zoom_callback(self):
        if self.zoom_active:
            self.zoom_active = False
        elif self.pan_active:
            self.zoom_active = True
            self.pan_active = False
        else:
            self.zoom_active = True
        self.handle_connection()

    def home_callback(self):
        self.canvas.draw()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.canvas.set_tangent()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.canvas.unset_tangent()
