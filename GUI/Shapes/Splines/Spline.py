import numpy as np
import pandas as pd

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

    def export(self, divisions=200, dx=True):
        if dx:
            x0 = self.x_coords[0]
            x1 = self.x_coords[-1]

            x = [x0 + i * (x1 - x0) / divisions for i in range(divisions)] + [self.x_coords[-1]]
            y = [self.spline.y_x(xi, 1e-12) for xi in x[:-1]] + [self.spline.y_t(1.)]
        else:
            x, y = self.spline.graph(1 / divisions)

        return {"graph": pd.DataFrame({"X": x, "Y": y}),
                "cp": pd.DataFrame({"X": self.x_coords, "Y": self.y_coords})}
