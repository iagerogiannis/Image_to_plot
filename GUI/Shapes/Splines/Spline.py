import numpy as np

from numerical_analysis.splines.bezier import Bezier
from GUI.Shapes.Shape import Shape


class Spline(Shape):

    def __init__(self, parent, control_x, control_y, color_cp, color_graph, plot_style_cp="o-", plot_style_graph="-"):
        super().__init__(parent, control_x, control_y, color_cp, plot_style_cp)
        self.color = [color_cp, color_graph]
        self.plot_style = [plot_style_cp, plot_style_graph]
        self.spline = Bezier(np.array([self.x_coords, self.y_coords]).transpose())
        self.graph = [[self.x_coords, self.y_coords], self.spline.graph(0.01)]

    def modify_point(self, point_index, point):
        self.x_coords[point_index] = point[0]
        self.y_coords[point_index] = point[1]
        self.spline.modify_control_point(point_index, point)
        self.graph[1] = self.spline.graph(0.01)
