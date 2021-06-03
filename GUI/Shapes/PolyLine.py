from GUI.Shapes.Shape import Shape


class PolyLine(Shape):

    def __init__(self, parent, x_coords, y_coords, color, plot_style="o-"):
        super().__init__(parent, x_coords, y_coords, color, plot_style)

    def append_point(self, point):
        super().append_point(point)
        self.graph = [[self.x_coords, self.y_coords]]
