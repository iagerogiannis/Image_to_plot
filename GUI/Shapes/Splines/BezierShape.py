import numpy as np

from GUI.Shapes.Splines.Spline import Spline
from numerical_analysis.splines import Bezier


class BezierShape(Spline):

    def __init__(self, parent, control_x, control_y, color_cp, color_graph, plot_style_cp="o-", plot_style_graph="-"):
        super().__init__(parent, control_x, control_y, color_cp, color_graph, plot_style_cp, plot_style_graph)

    def append_point(self, point):
        super().append_point(point)
        self.spline = Bezier(np.array([self.x_coords, self.y_coords]).transpose())
        self.graph = [[self.x_coords, self.y_coords], self.spline.graph(0.01)]
