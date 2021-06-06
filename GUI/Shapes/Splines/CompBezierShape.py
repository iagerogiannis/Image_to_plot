from GUI.Shapes.Splines.Spline import Spline
from numerical_analysis.splines import *
from numerical_analysis.dependencies import StraightLine


class CompBezierShape(Spline):

    def __init__(self, parent, control_x, control_y, order, color_cp, color_graph, plot_style_cp="o-",
                 plot_style_graph="-"):
        super().__init__(parent, control_x, control_y, color_cp, color_graph, plot_style_cp, plot_style_graph)
        self.order = order
        self.spline = CompositeBezier(np.array([self.x_coords, self.y_coords]).transpose(), self.order)
        self.graph = [self.spline.graph_cp(), self.spline.graph(0.01)]

    def modify_point(self, index, point, called_by_recursion=False):

        self.spline.modify_control_point(index, point, tangent_links=True)
        self.x_coords, self.y_coords = self.spline.cp.transpose().tolist()
        self.graph = [self.spline.graph_cp(), self.spline.graph(0.01)]

    def append_point(self, point):
        super().append_point(point)
        self.spline = CompositeBezier(np.array([self.x_coords, self.y_coords]).transpose(), self.order)
        self.graph = [[self.x_coords, self.y_coords], self.spline.graph(0.01)]


class CompQuadBezierShape(CompBezierShape):

    def __init__(self, parent, control_x, control_y, color_cp, color_graph, plot_style_cp="o-", plot_style_graph="-"):
        super().__init__(parent, control_x, control_y, 2, color_cp, color_graph, plot_style_cp, plot_style_graph)
        self.spline = CompositeQuadraticBezier(np.array([self.x_coords, self.y_coords]).transpose())
        self.graph = [[self.x_coords, self.y_coords], self.spline.graph(0.01)]

    def modify_point(self, index, point, called_by_recursion=False):
        x_diff = point[0] - self.x_coords[index]
        y_diff = point[1] - self.y_coords[index]
        self.x_coords[index] += x_diff
        self.y_coords[index] += y_diff
        self.spline.modify_control_point(index, point)
        self.graph[1] = self.spline.graph(0.01)

    def append_point(self, point):
        self.x_coords.append(point[0])
        self.y_coords.append(point[1])
        self.spline = CompositeQuadraticBezier(np.array([self.x_coords, self.y_coords]).transpose())
        self.graph = [[self.x_coords, self.y_coords], self.spline.graph(0.01)]


class CompCubBezierShape(CompBezierShape):

    def __init__(self, parent, control_x, control_y, color_cp, color_graph, plot_style_cp="o-", plot_style_graph="-"):
        super().__init__(parent, control_x, control_y, 3, color_cp, color_graph, plot_style_cp, plot_style_graph)

    def append_point(self, point):
        line = StraightLine([[-1, [self.x_coords[-2], self.y_coords[-2]]], [0, [self.x_coords[-1], self.y_coords[-1]]]])
        new_point = line.point_t(1)
        self.x_coords.append(new_point[0])
        self.y_coords.append(new_point[1])
        self.x_coords.append(point[0])
        self.y_coords.append(point[1])
        super().append_point(point)
